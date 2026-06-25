<script setup>
import axios from "axios";
import { onMounted, reactive, ref } from "vue";

import Navbar from "../components/Navbar.vue";
import Sidebar from "../components/Sidebar.vue";
import { useAuthStore } from "../stores/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const authStore = useAuthStore();

const courses = ref([]);
const newCourse = reactive({ title: "", description: "" });
const lessonsByCourse = reactive({});
const expandedCourse = ref(null);
const newLesson = reactive({ title: "", content: "" });
const activeLessonForm = ref(null);
const newQuestion = reactive({ text: "", reference_answer: "", question_type: "open_text" });
const error = ref("");

async function loadCourses() {
  try {
    const { data } = await axios.get(`${API_BASE_URL}/courses`);
    courses.value = data;
  } catch (e) {
    console.error("Ошибка загрузки курсов:", e.response?.data ?? e.message);
  }
}

async function createCourse() {
  error.value = "";
  try {
    await axios.post(
      `${API_BASE_URL}/courses?teacher_id=${authStore.user?.id}`,
      { title: newCourse.title, description: newCourse.description },
    );
    newCourse.title = "";
    newCourse.description = "";
    await loadCourses();
  } catch (e) {
    error.value = "Не удалось создать курс";
    console.error("Ошибка создания курса:", e.response?.data ?? e.message);
  }
}

async function toggleCourse(courseId) {
  if (expandedCourse.value === courseId) {
    expandedCourse.value = null;
    return;
  }
  expandedCourse.value = courseId;
  await loadLessons(courseId);
}

async function loadLessons(courseId) {
  try {
    const { data } = await axios.get(`${API_BASE_URL}/lessons?course_id=${courseId}`);
    lessonsByCourse[courseId] = data;
  } catch (e) {
    console.error("Ошибка загрузки уроков:", e.response?.data ?? e.message);
  }
}

async function addLesson(courseId) {
  try {
    await axios.post(
      `${API_BASE_URL}/lessons?course_id=${courseId}`,
      { title: newLesson.title, content: newLesson.content },
    );
    newLesson.title = "";
    newLesson.content = "";
    await loadLessons(courseId);
  } catch (e) {
    console.error("Ошибка добавления урока:", e.response?.data ?? e.message);
  }
}

function toggleQuestionForm(lessonId) {
  activeLessonForm.value = activeLessonForm.value === lessonId ? null : lessonId;
  newQuestion.text = "";
  newQuestion.reference_answer = "";
  newQuestion.question_type = "open_text";
}

async function addQuestion(lessonId) {
  try {
    await axios.post(`${API_BASE_URL}/questions?lesson_id=${lessonId}`, {
      text: newQuestion.text,
      reference_answer: newQuestion.reference_answer,
      question_type: newQuestion.question_type,
    });
    activeLessonForm.value = null;
  } catch (e) {
    console.error("Ошибка добавления вопроса:", e.response?.data ?? e.message);
  }
}

onMounted(loadCourses);
</script>

<template>
  <div class="flex min-h-screen bg-bg">
    <Sidebar />

    <div class="flex-1">
      <Navbar title="Редактор курсов" />

      <main class="space-y-6 p-6">
        <div class="card p-6">
          <h2 class="mb-4 text-sm font-medium text-text/70">Создать курс</h2>
          <div class="space-y-3">
            <input v-model="newCourse.title" placeholder="Название курса" class="input-field" />
            <textarea
              v-model="newCourse.description"
              placeholder="Описание курса"
              class="input-field min-h-[80px] resize-none"
            ></textarea>
            <button class="btn-primary" @click="createCourse">Создать курс</button>
            <p v-if="error" class="text-sm text-red-400">{{ error }}</p>
          </div>
        </div>

        <div class="space-y-3">
          <h2 class="text-sm font-medium text-text/70">Существующие курсы</h2>
          <p v-if="courses.length === 0" class="text-sm text-text/40">Курсов пока нет</p>

          <div v-for="course in courses" :key="course.id" class="card p-5">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-semibold text-text">{{ course.title }}</h3>
                <p class="text-sm text-text/60">{{ course.description || "Без описания" }}</p>
              </div>
              <button
                class="rounded-lg bg-white/5 px-3 py-1.5 text-sm text-text/80 transition-all duration-200 hover:bg-white/10"
                @click="toggleCourse(course.id)"
              >
                {{ expandedCourse === course.id ? "Свернуть" : "Уроки" }}
              </button>
            </div>

            <div v-if="expandedCourse === course.id" class="mt-4 space-y-3 border-t border-white/5 pt-4">
              <div
                v-for="lesson in lessonsByCourse[course.id] || []"
                :key="lesson.id"
                class="rounded-xl bg-bg p-3"
              >
                <div class="flex items-center justify-between">
                  <span class="text-sm text-text">{{ lesson.title }}</span>
                  <button
                    class="text-xs text-accent-light hover:underline"
                    @click="toggleQuestionForm(lesson.id)"
                  >
                    + вопрос
                  </button>
                </div>

                <div v-if="activeLessonForm === lesson.id" class="mt-3 space-y-2">
                  <input
                    v-model="newQuestion.text"
                    placeholder="Текст вопроса"
                    class="input-field"
                  />
                  <input
                    v-model="newQuestion.reference_answer"
                    placeholder="Правильный ответ"
                    class="input-field"
                  />
                  <select v-model="newQuestion.question_type" class="input-field">
                    <option value="open_text">Открытый</option>
                    <option value="single_choice">Тест</option>
                  </select>
                  <button class="btn-primary" @click="addQuestion(lesson.id)">
                    Добавить вопрос
                  </button>
                </div>
              </div>

              <div class="space-y-2 rounded-xl bg-bg p-3">
                <p class="text-xs font-medium text-text/50">Новый урок</p>
                <input v-model="newLesson.title" placeholder="Название урока" class="input-field" />
                <textarea
                  v-model="newLesson.content"
                  placeholder="Содержание урока"
                  class="input-field min-h-[60px] resize-none"
                ></textarea>
                <button
                  class="rounded-lg bg-accent/15 px-3 py-1.5 text-sm text-accent-light transition-all duration-200 hover:bg-accent/25"
                  @click="addLesson(course.id)"
                >
                  Добавить урок
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
