import axios from "axios";
import { defineStore } from "pinia";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("access_token") || null,
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },

  actions: {
    async login(email, password) {
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, {
        email,
        password,
      });
      this.token = response.data.access_token;
      localStorage.setItem("access_token", this.token);
    },

    async register(email, password, fullName, role) {
      await axios.post(`${API_BASE_URL}/api/auth/register`, {
        email,
        password,
        full_name: fullName,
        role,
      });
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("access_token");
    },
  },
});
