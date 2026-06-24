import axios from "axios";
import { defineStore } from "pinia";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const useLessonStore = defineStore("lesson", {
  state: () => ({
    currentLesson: null,
    currentSessionId: null,
    recommendedDifficulty: "same",
  }),

  actions: {
    async fetchLesson(lessonId) {
      const response = await axios.get(`${API_BASE_URL}/api/lessons/${lessonId}`);
      this.currentLesson = response.data;
    },

    async startSession(studentId, lessonId) {
      const response = await axios.post(
        `${API_BASE_URL}/api/sessions?student_id=${studentId}`,
        { lesson_id: lessonId },
      );
      this.currentSessionId = response.data.id;
    },

    async submitAnswer(questionId, text) {
      const response = await axios.post(
        `${API_BASE_URL}/api/sessions/${this.currentSessionId}/answer`,
        { question_id: questionId, text },
      );
      return response.data;
    },

    async fetchNextDifficulty() {
      const response = await axios.get(
        `${API_BASE_URL}/api/sessions/${this.currentSessionId}/next-lesson`,
      );
      this.recommendedDifficulty = response.data.recommended_difficulty;
    },
  },
});
