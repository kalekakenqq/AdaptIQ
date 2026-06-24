<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

const email = ref("");
const password = ref("");
const fullName = ref("");
const role = ref("student");
const error = ref("");
const loading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

async function handleRegister() {
  error.value = "";
  loading.value = true;
  try {
    await authStore.register(email.value, password.value, fullName.value, role.value);
    router.push({ name: "login" });
  } catch (e) {
    error.value = "Не удалось зарегистрироваться";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-bg px-4">
    <div class="w-full max-w-sm">
      <div class="mb-8 flex items-center justify-center gap-2">
        <svg
          class="h-8 w-8 text-accent-light"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            d="M9.5 2a3.5 3.5 0 0 0-3.5 3.5v1.05A3.5 3.5 0 0 0 4 9.78v1.69a3 3 0 0 0-1 2.24V16a3 3 0 0 0 3 3h.17A3.5 3.5 0 0 0 9.5 22h1a3.5 3.5 0 0 0 3.43-2.84A3.5 3.5 0 0 0 17 16v-1a3 3 0 0 0-1-2.24V11a3.5 3.5 0 0 0-2-3.16V5.5A3.5 3.5 0 0 0 10.5 2h-1Z"
          />
        </svg>
        <span class="text-2xl font-bold tracking-tight text-text">AdaptIQ</span>
      </div>

      <div class="card p-8">
        <h1 class="mb-6 text-center text-xl font-semibold text-text">Создать аккаунт</h1>

        <form class="space-y-4" @submit.prevent="handleRegister">
          <div>
            <label class="mb-1.5 block text-sm text-text/70">Полное имя</label>
            <input v-model="fullName" type="text" class="input-field" required />
          </div>
          <div>
            <label class="mb-1.5 block text-sm text-text/70">Email</label>
            <input v-model="email" type="email" class="input-field" required />
          </div>
          <div>
            <label class="mb-1.5 block text-sm text-text/70">Пароль</label>
            <input v-model="password" type="password" class="input-field" required />
          </div>
          <div>
            <label class="mb-1.5 block text-sm text-text/70">Роль</label>
            <select v-model="role" class="input-field">
              <option value="student">Студент</option>
              <option value="teacher">Преподаватель</option>
            </select>
          </div>

          <p v-if="error" class="text-sm text-red-400">{{ error }}</p>

          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? "Регистрируем..." : "Зарегистрироваться" }}
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-text/60">
          Уже есть аккаунт?
          <router-link to="/login" class="font-medium text-accent-light hover:underline">
            Войти
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>
