<script setup>
import { ref } from "vue";

import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const lessonId = ref("");
const summary = ref(null);

async function loadSummary() {
  const response = await axios.get(`${API_BASE_URL}/api/reports/lesson/${lessonId.value}/summary`);
  summary.value = response.data;
}
</script>

<template>
  <div class="teacher-dashboard">
    <h1>Личный кабинет преподавателя</h1>
    <input v-model="lessonId" placeholder="ID урока" />
    <button @click="loadSummary">Загрузить отчёт</button>
    <div v-if="summary">
      <p>Количество сессий: {{ summary.sessions_count }}</p>
      <p>Средний балл: {{ summary.average_score.toFixed(2) }}</p>
    </div>
    <router-link to="/courses/editor">Редактор курсов</router-link>
  </div>
</template>
