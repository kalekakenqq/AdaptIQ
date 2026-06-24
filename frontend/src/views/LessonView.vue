<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useRoute } from "vue-router";

import Camera from "../components/Camera.vue";
import { useAuthStore } from "../stores/auth";
import { useLessonStore } from "../stores/lesson";

const route = useRoute();
const authStore = useAuthStore();
const lessonStore = useLessonStore();

const answerText = ref("");
const questionId = ref(route.query.questionId || "");
const lastResult = ref(null);
const cognitiveLoadIndex = ref(0);
const riskScore = ref(3.2);

const violations = ref([
  { label: "Потеря концентрации", time: "00:02:14" },
  { label: "Отвлечение от экрана", time: "00:05:41" },
]);

const questionNumber = ref(1);
const totalQuestions = ref(8);
const progressPercent = computed(() => (questionNumber.value / totalQuestions.value) * 100);

const elapsedSeconds = ref(0);
let timerHandle = null;
const formattedTime = computed(() => {
  const minutes = String(Math.floor(elapsedSeconds.value / 60)).padStart(2, "0");
  const seconds = String(elapsedSeconds.value % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
});

const riskGradientPosition = computed(() => Math.min(riskScore.value / 10, 1) * 100);

onMounted(async () => {
  await lessonStore.fetchLesson(route.params.id);
  await lessonStore.startSession(authStore.user?.id, route.params.id);
  timerHandle = setInterval(() => {
    elapsedSeconds.value += 1;
  }, 1000);
});

onUnmounted(() => {
  if (timerHandle) clearInterval(timerHandle);
});

async function handleAnswerSubmit() {
  lastResult.value = await lessonStore.submitAnswer(questionId.value, answerText.value);
  await lessonStore.fetchNextDifficulty();
}

function onCognitiveLoadUpdate(index) {
  cognitiveLoadIndex.value = index;
}
</script>

<template>
  <div class="min-h-screen bg-bg p-6">
    <div class="mx-auto flex max-w-5xl items-start justify-between gap-6">
      <div class="flex-1 space-y-4">
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

      <div class="w-72 shrink-0 space-y-4">
        <div class="card flex items-center justify-center gap-2 p-3">
          <svg class="h-4 w-4 text-accent-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 7v5l3 3" />
          </svg>
          <span class="font-mono text-sm text-text">{{ formattedTime }}</span>
        </div>

        <div class="card p-4">
          <Camera
            v-if="lessonStore.currentSessionId"
            :session-id="lessonStore.currentSessionId"
            class="overflow-hidden rounded-xl"
            @cognitive-load-update="onCognitiveLoadUpdate"
          />
        </div>

        <div class="card p-4">
          <h3 class="mb-2 text-sm font-medium text-text/70">Risk Score</h3>
          <div class="h-2 w-full rounded-full bg-gradient-to-r from-green-500 via-yellow-400 to-red-500">
            <div
              class="relative h-2 w-2 -translate-y-1/2 rounded-full border-2 border-white bg-bg"
              :style="{ marginLeft: `${riskGradientPosition}%`, top: '50%' }"
            ></div>
          </div>
          <p class="mt-2 text-sm text-text/70">{{ riskScore.toFixed(1) }} / 10</p>
        </div>

        <div class="card p-4">
          <h3 class="mb-2 text-sm font-medium text-text/70">Нарушения</h3>
          <ul class="space-y-2">
            <li v-for="violation in violations" :key="violation.time" class="flex items-center gap-2 text-sm text-text/70">
              <svg class="h-4 w-4 shrink-0 text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 9v4m0 4h.01M10.29 3.86l-8.18 14.18A1 1 0 0 0 3 19.5h18a1 1 0 0 0 .89-1.46L13.71 3.86a1 1 0 0 0-1.42 0Z" />
              </svg>
              <span class="flex-1">{{ violation.label }}</span>
              <span class="font-mono text-text/40">{{ violation.time }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
