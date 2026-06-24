<script setup>
import { onMounted } from "vue";

import RiskScore from "../components/RiskScore.vue";
import { useAnalyticsStore } from "../stores/analytics";
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
const analyticsStore = useAnalyticsStore();

onMounted(() => {
  if (authStore.user?.id) {
    analyticsStore.fetchRiskScore(authStore.user.id);
  }
});
</script>

<template>
  <div class="student-dashboard">
    <h1>Личный кабинет студента</h1>
    <RiskScore :score="analyticsStore.riskScore?.risk_score || 0" />
    <router-link to="/analytics">Подробная аналитика</router-link>
  </div>
</template>
