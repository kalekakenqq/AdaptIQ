<script setup>
import { Chart, registerables } from "chart.js";
import { onMounted, ref } from "vue";

import RiskScore from "../components/RiskScore.vue";
import { useAnalyticsStore } from "../stores/analytics";
import { useAuthStore } from "../stores/auth";

Chart.register(...registerables);

const authStore = useAuthStore();
const analyticsStore = useAnalyticsStore();
const chartCanvas = ref(null);

onMounted(async () => {
  if (!authStore.user?.id) return;

  await analyticsStore.fetchRiskScore(authStore.user.id);
  await analyticsStore.fetchHistory(authStore.user.id);

  new Chart(chartCanvas.value, {
    type: "line",
    data: {
      labels: analyticsStore.history.map((item) => item.recorded_at),
      datasets: [
        {
          label: "Когнитивная нагрузка",
          data: analyticsStore.history.map((item) => item.cognitive_load_index),
          borderColor: "#ff7043",
        },
        {
          label: "Риск-оценка",
          data: analyticsStore.history.map((item) => item.risk_score),
          borderColor: "#42a5f5",
        },
      ],
    },
  });
});
</script>

<template>
  <div class="analytics-view">
    <h1>Аналитика</h1>
    <RiskScore :score="analyticsStore.riskScore?.risk_score || 0" />
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>
