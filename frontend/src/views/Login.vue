<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

const email = ref("");
const password = ref("");
const error = ref("");

const authStore = useAuthStore();
const router = useRouter();

async function handleLogin() {
  error.value = "";
  try {
    await authStore.login(email.value, password.value);
    router.push({ name: "student-dashboard" });
  } catch (e) {
    error.value = "неверный email или пароль";
  }
}
</script>

<template>
  <div class="login-page">
    <h1>Вход в AdaptIQ</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <button type="submit">Войти</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <router-link to="/register">Регистрация</router-link>
  </div>
</template>
