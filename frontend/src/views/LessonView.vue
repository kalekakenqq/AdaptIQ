<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import Camera from "../components/Camera.vue";
import CognitiveLoad from "../components/CognitiveLoad.vue";
import { useAuthStore } from "../stores/auth";
import { useLessonStore } from "../stores/lesson";

const route = useRoute();
const authStore = useAuthStore();
const lessonStore = useLessonStore();

const answerText = ref("");
const questionId = ref(route.query.questionId || "");
const lastResult = ref(null);
const cognitiveLoadIndex = ref(0);

onMounted(async () => {
  await lessonStore.fetchLesson(route.params.id);
  await lessonStore.startSession(authStore.user?.id, route.params.id);
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
  <div class="lesson-view">
    <h1>{{ lessonStore.currentLesson?.title }}</h1>
    <p>{{ lessonStore.currentLesson?.content }}</p>

    <Camera
      v-if="lessonStore.currentSessionId"
      :session-id="lessonStore.currentSessionId"
      @cognitive-load-update="onCognitiveLoadUpdate"
    />
    <CognitiveLoad :index="cognitiveLoadIndex" />

    <textarea v-model="answerText" placeholder="Введите ваш ответ"></textarea>
    <button @click="handleAnswerSubmit">Отправить ответ</button>
    <p v-if="lastResult">Оценка: {{ lastResult.score }}</p>
    <p>Рекомендованная сложность следующего шага: {{ lessonStore.recommendedDifficulty }}</p>
  </div>
</template>
