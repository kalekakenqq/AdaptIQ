<script setup>
import { computed, onMounted, ref } from "vue";

import { useAuthStore } from "../stores/auth";

const STORAGE_KEY = "adaptiq_onboarding_done";

const authStore = useAuthStore();
const visible = ref(false);
const step = ref(0);

const steps = [
  {
    title: "Добро пожаловать в AdaptIQ",
    text: "Адаптивная образовательная платформа с ИИ, которая подстраивается под ваше состояние и темп обучения.",
  },
  {
    title: "Как работает граф знаний",
    text: "Темы курса связаны в граф. Цвет узла показывает уровень усвоения: зелёный — освоено, жёлтый — в процессе, красный — требует внимания.",
  },
  {
    title: "Как работает адаптация",
    text: "Во время урока система анализирует ваши ответы и поведение через камеру, а RL-агент подбирает оптимальную сложность следующего материала.",
  },
];

const current = computed(() => steps[step.value]);
const isLast = computed(() => step.value === steps.length - 1);

function finish() {
  localStorage.setItem(STORAGE_KEY, "1");
  visible.value = false;
}

function next() {
  if (isLast.value) finish();
  else step.value += 1;
}

onMounted(() => {
  if (authStore.isAuthenticated && !localStorage.getItem(STORAGE_KEY)) {
    visible.value = true;
  }
});
</script>

<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
  >
    <div class="card w-full max-w-md p-8 text-center">
      <div class="mb-5 flex justify-center gap-1.5">
        <span
          v-for="(s, idx) in steps"
          :key="idx"
          class="h-1.5 rounded-full transition-all duration-200"
          :class="idx === step ? 'w-6 bg-accent' : 'w-1.5 bg-white/20'"
        ></span>
      </div>

      <h2 class="text-xl font-bold text-text">{{ current.title }}</h2>
      <p class="mt-3 text-sm text-text/70">{{ current.text }}</p>

      <div class="mt-6 flex items-center justify-between">
        <button class="text-sm text-text/50 hover:text-text/80" @click="finish">Пропустить</button>
        <button class="btn-primary w-auto px-6" @click="next">
          {{ isLast ? "Начать" : "Далее" }}
        </button>
      </div>
    </div>
  </div>
</template>
