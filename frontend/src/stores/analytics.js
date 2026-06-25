import axios from "axios";
import { defineStore } from "pinia";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

export const useAnalyticsStore = defineStore("analytics", {
  state: () => ({
    riskScore: null,
    history: [],
    cognitiveLoadIndex: 0,
  }),

  actions: {
    async fetchRiskScore(studentId) {
      const response = await axios.get(`${API_BASE_URL}/analytics/risk/${studentId}`);
      this.riskScore = response.data;
    },

    async fetchHistory(studentId) {
      const response = await axios.get(`${API_BASE_URL}/analytics/history/${studentId}`);
      this.history = response.data;
    },

    setCognitiveLoadIndex(value) {
      this.cognitiveLoadIndex = value;
    },
  },
});
