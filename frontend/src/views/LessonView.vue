<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useRoute } from "vue-router";

import { useAuthStore } from "../stores/auth";
import { useLessonStore } from "../stores/lesson";

const MEDIAPIPE_SRC = "https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/face_detection.js";
const ANALYZE_INTERVAL_MS = 100;
const VIOLATION_COOLDOWN_MS = 3000;
const YAW_THRESHOLD_DEG = 30;

const route = useRoute();
const authStore = useAuthStore();
const lessonStore = useLessonStore();

const answerText = ref("");
const questionId = ref(route.query.questionId || "");
const lastResult = ref(null);

const videoRef = ref(null);
const cameraStatus = ref("инициализация камеры...");
const riskScore = ref(0);
const violations = ref([]);

const questionNumber = ref(1);
const totalQuestions = ref(8);
const progressPercent = computed(() => (questionNumber.value / totalQuestions.value) * 100);

const elapsedSeconds = ref(0);
const formattedTime = computed(() => {
  const minutes = String(Math.floor(elapsedSeconds.value / 60)).padStart(2, "0");
  const seconds = String(elapsedSeconds.value % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
});

const riskGradientPosition = computed(() => Math.min(riskScore.value / 10, 1) * 100);

const VIOLATION_META = {
  face_absent: { label: "Лицо не обнаружено", risk: 3 },
  face_away: { label: "Взгляд отведён от экрана", risk: 1 },
  multiple_faces: { label: "В кадре несколько лиц", risk: 5 },
};

let timerHandle = null;
let analyzeHandle = null;
let mediaStream = null;
let faceDetection = null;
let wsConnection = null;
let processing = false;
const lastViolationAt = {};

function loadMediaPipeScript() {
  return new Promise((resolve, reject) => {
    if (window.FaceDetection) {
      resolve();
      return;
    }
    const script = document.createElement("script");
    script.src = MEDIAPIPE_SRC;
    script.crossOrigin = "anonymous";
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("не удалось загрузить MediaPipe"));
    document.head.appendChild(script);
  });
}

function connectWebSocket(sessionId) {
  try {
    const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
    wsConnection = new WebSocket(`${proto}//${window.location.host}/ws/${sessionId}`);
    wsConnection.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (typeof data.risk_score === "number") {
        riskScore.value = data.risk_score;
      }
    };
  } catch (error) {
    console.warn("WebSocket прокторинга недоступен:", error);
  }
}

function sendEvent(type) {
  if (wsConnection && wsConnection.readyState === WebSocket.OPEN) {
    wsConnection.send(JSON.stringify({ type, timestamp: Date.now() }));
  }
}

function registerViolation(type) {
  const now = Date.now();
  if (lastViolationAt[type] && now - lastViolationAt[type] < VIOLATION_COOLDOWN_MS) {
    return;
  }
  lastViolationAt[type] = now;

  const meta = VIOLATION_META[type];
  riskScore.value = Math.min(10, riskScore.value + meta.risk);
  violations.value.unshift({
    type,
    label: meta.label,
    time: formattedTime.value,
  });
  if (violations.value.length > 20) {
    violations.value.pop();
  }
  sendEvent(type);
}

function getKeypoints(detection) {
  if (detection.landmarks) return detection.landmarks;
  if (detection.keypoints) return detection.keypoints;
  if (detection.locationData?.relativeKeypoints) return detection.locationData.relativeKeypoints;
  return null;
}

function estimateYaw(keypoints) {
  const rightEye = keypoints[0];
  const leftEye = keypoints[1];
  const nose = keypoints[2];
  if (!rightEye || !leftEye || !nose) return 0;
  const eyeCenterX = (rightEye.x + leftEye.x) / 2;
  const eyeDist = Math.abs(leftEye.x - rightEye.x) || 0.0001;
  return ((nose.x - eyeCenterX) / eyeDist) * 90;
}

function onFaceResults(results) {
  const detections = results.detections || [];

  if (detections.length === 0) {
    cameraStatus.value = "лицо не обнаружено";
    registerViolation("face_absent");
    return;
  }

  if (detections.length >= 2) {
    cameraStatus.value = "несколько лиц в кадре";
    registerViolation("multiple_faces");
    return;
  }

  const keypoints = getKeypoints(detections[0]);
  const yaw = keypoints ? estimateYaw(keypoints) : 0;
  if (Math.abs(yaw) > YAW_THRESHOLD_DEG) {
    cameraStatus.value = "взгляд отведён";
    registerViolation("face_away");
  } else {
    cameraStatus.value = "контроль активен";
    riskScore.value = Math.max(0, riskScore.value - 0.05);
  }
}

// загружает MediaPipe FaceDetection через CDN только после старта видео
async function startMediaPipe() {
  try {
    await loadMediaPipeScript();
    faceDetection = new window.FaceDetection({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/${file}`,
    });
    faceDetection.setOptions({ model: "short", minDetectionConfidence: 0.5 });
    faceDetection.onResults(onFaceResults);

    analyzeHandle = setInterval(async () => {
      if (processing || !videoRef.value || videoRef.value.readyState < 2) return;
      processing = true;
      try {
        await faceDetection.send({ image: videoRef.value });
      } catch (error) {
        console.warn("ошибка анализа кадра:", error);
      } finally {
        processing = false;
      }
    }, ANALYZE_INTERVAL_MS);
  } catch (error) {
    console.error("MediaPipe:", error);
  }
}

async function initCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    videoRef.value.srcObject = stream;
    mediaStream = stream;
    await videoRef.value.play();
    cameraStatus.value = "камера активна";
    startMediaPipe();
  } catch (e) {
    cameraStatus.value = "нет доступа к камере: " + e.message;
    console.error("камера:", e);
  }
}

onMounted(async () => {
  await lessonStore.fetchLesson(route.params.id);
  await lessonStore.startSession(authStore.user?.id, route.params.id);

  timerHandle = setInterval(() => {
    elapsedSeconds.value += 1;
  }, 1000);

  if (lessonStore.currentSessionId) {
    connectWebSocket(lessonStore.currentSessionId);
  }
  await initCamera();
});

onUnmounted(() => {
  if (timerHandle) clearInterval(timerHandle);
  if (analyzeHandle) clearInterval(analyzeHandle);
  if (mediaStream) mediaStream.getTracks().forEach((track) => track.stop());
  if (faceDetection) faceDetection.close?.();
  if (wsConnection) wsConnection.close();
});

async function handleAnswerSubmit() {
  lastResult.value = await lessonStore.submitAnswer(questionId.value, answerText.value);
  await lessonStore.fetchNextDifficulty();
}
</script>

<template>
  <div class="min-h-screen bg-bg p-6">
    <div class="mx-auto flex max-w-5xl flex-col items-start gap-6 lg:flex-row lg:justify-between">
      <div class="w-full flex-1 space-y-4">
        <div class="card p-8">
          <div class="mb-4 flex items-center justify-between">
            <span class="text-sm font-medium text-text/60">
              Вопрос {{ questionNumber }} из {{ totalQuestions }}
            </span>
            <div class="h-1.5 w-40 overflow-hidden rounded-full bg-white/10">
              <div
                class="h-full rounded-full bg-gradient-to-r from-accent to-accent-light transition-all duration-200"
                :style="{ width: `${progressPercent}%` }"
              ></div>
            </div>
          </div>

          <h1 class="text-lg font-semibold text-text">{{ lessonStore.currentLesson?.title }}</h1>
          <p class="mt-2 text-text/70">{{ lessonStore.currentLesson?.content }}</p>

          <textarea
            v-model="answerText"
            placeholder="Введите ваш ответ"
            class="input-field mt-5 min-h-[120px] resize-none"
          ></textarea>

          <button class="btn-primary mt-4" @click="handleAnswerSubmit">Отправить ответ</button>

          <p v-if="lastResult" class="mt-3 text-sm text-text/70">Оценка: {{ lastResult.score }}</p>
          <p class="mt-1 text-sm text-text/50">
            Рекомендованная сложность следующего шага: {{ lessonStore.recommendedDifficulty }}
          </p>
        </div>
      </div>

      <div class="w-full shrink-0 space-y-4 lg:w-72">
        <div class="card flex items-center justify-center gap-2 p-3">
          <svg
            class="h-4 w-4 text-accent-light"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="12" cy="12" r="9" />
            <path d="M12 7v5l3 3" />
          </svg>
          <span class="font-mono text-sm text-text">{{ formattedTime }}</span>
        </div>

        <div class="card overflow-hidden p-4">
          <h3 class="mb-2 text-sm font-medium text-text/70">Прокторинг</h3>
          <div class="relative overflow-hidden rounded-xl bg-black">
            <video
              ref="videoRef"
              autoplay
              muted
              playsinline
              class="h-44 w-full -scale-x-100 object-cover"
            ></video>
          </div>
          <p
            class="mt-2 flex items-center gap-1.5 text-xs"
            :class="cameraStatus === 'камера активна' ? 'text-green-400' : 'text-text/50'"
          >
            <span
              class="inline-block h-2 w-2 rounded-full"
              :class="cameraStatus === 'камера активна' ? 'bg-green-400' : 'bg-text/40'"
            ></span>
            {{ cameraStatus }}
          </p>
        </div>

        <div class="card p-4">
          <h3 class="mb-2 text-sm font-medium text-text/70">Risk Score</h3>
          <div
            class="relative h-2 w-full rounded-full bg-gradient-to-r from-green-500 via-yellow-400 to-red-500"
          >
            <div
              class="absolute top-1/2 h-3.5 w-3.5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-bg transition-all duration-300"
              :style="{ left: `${riskGradientPosition}%` }"
            ></div>
          </div>
          <p class="mt-2 text-sm text-text/70">{{ riskScore.toFixed(1) }} / 10</p>
        </div>

        <div class="card p-4">
          <h3 class="mb-2 text-sm font-medium text-text/70">Нарушения</h3>
          <ul v-if="violations.length" class="space-y-2">
            <li
              v-for="(violation, idx) in violations"
              :key="idx"
              class="flex items-center gap-2 text-sm text-text/70"
            >
              <svg
                class="h-4 w-4 shrink-0 text-red-400"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  d="M12 9v4m0 4h.01M10.29 3.86l-8.18 14.18A1 1 0 0 0 3 19.5h18a1 1 0 0 0 .89-1.46L13.71 3.86a1 1 0 0 0-1.42 0Z"
                />
              </svg>
              <span class="flex-1">{{ violation.label }}</span>
              <span class="font-mono text-text/40">{{ violation.time }}</span>
            </li>
          </ul>
          <p v-else class="text-sm text-text/40">Нарушений не зафиксировано</p>
        </div>
      </div>
    </div>
  </div>
</template>
