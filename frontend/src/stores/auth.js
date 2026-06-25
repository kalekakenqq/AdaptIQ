import axios from "axios";
import { defineStore } from "pinia";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

// декодирует payload JWT с корректной обработкой UTF-8 (кириллица)
function decodeJwt(token) {
  try {
    const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
    const json = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + c.charCodeAt(0).toString(16).padStart(2, "0"))
        .join(""),
    );
    return JSON.parse(json);
  } catch (error) {
    console.warn("не удалось декодировать JWT:", error);
    return null;
  }
}

function userFromToken(token) {
  if (!token) return null;
  const payload = decodeJwt(token);
  if (!payload) return null;
  return {
    id: payload.sub,
    full_name: payload.name || "Пользователь",
    role: payload.role || "student",
  };
}

export const useAuthStore = defineStore("auth", {
  state: () => {
    const token = localStorage.getItem("access_token") || null;
    return {
      token,
      user: userFromToken(token),
    };
  },

  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    isTeacher: (state) => state.user?.role === "teacher",
  },

  actions: {
    setToken(token) {
      this.token = token;
      this.user = userFromToken(token);
      localStorage.setItem("access_token", token);
    },

    async login(email, password) {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        email,
        password,
      });
      this.setToken(response.data.access_token);
    },

    async register(email, password, fullName, role) {
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/register`, {
          email,
          password,
          full_name: fullName,
          role,
        });
        this.setToken(response.data.access_token);
      } catch (error) {
        console.error("Ошибка регистрации, ответ сервера:", error.response?.data ?? error.message);
        throw error;
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("access_token");
    },
  },
});
