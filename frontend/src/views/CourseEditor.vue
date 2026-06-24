<script setup>
import axios from "axios";
import { ref } from "vue";

import { useAuthStore } from "../stores/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const authStore = useAuthStore();
const title = ref("");
const description = ref("");
const createdCourseId = ref(null);

async function createCourse() {
  const response = await axios.post(
    `${API_BASE_URL}/api/courses?teacher_id=${authStore.user?.id}`,
    { title: title.value, description: description.value },
  );
  createdCourseId.value = response.data.id;
}
</script>

<template>
  <div class="course-editor">
    <h1>Редактор курсов</h1>
    <input v-model="title" placeholder="Название курса" />
    <textarea v-model="description" placeholder="Описание курса"></textarea>
    <button @click="createCourse">Создать курс</button>
    <p v-if="createdCourseId">Курс создан: {{ createdCourseId }}</p>
  </div>
</template>
