<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

const email = ref("");
const password = ref("");
const fullName = ref("");
const role = ref("student");
const error = ref("");
const success = ref(false);

const authStore = useAuthStore();
const router = useRouter();

async function handleRegister() {
  error.value = "";
  try {
    await authStore.register(email.value, password.value, fullName.value, role.value);
    success.value = true;
    router.push({ name: "login" });
  } catch (e) {
    error.value = "не удалось зарегистрироваться";
  }
}
</script>

<template>
  <div class="register-page">
    <h1>Регистрация в AdaptIQ</h1>
    <form @submit.prevent="handleRegister">
      <input v-model="fullName" type="text" placeholder="Полное имя" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <select v-model="role">
        <option value="student">Студент</option>
        <option value="teacher">Преподаватель</option>
      </select>
      <button type="submit">Зарегистрироваться</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <router-link to="/login">Уже есть аккаунт? Войти</router-link>
  </div>
</template>
