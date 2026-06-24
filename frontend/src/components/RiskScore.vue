<script setup>
defineProps({
  score: {
    type: Number,
    default: 0,
  },
});

function riskLabel(score) {
  if (score < 0.33) return "низкий риск";
  if (score < 0.66) return "средний риск";
  return "высокий риск";
}

function riskColor(score) {
  if (score < 0.33) return "#4caf50";
  if (score < 0.66) return "#ff9800";
  return "#f44336";
}
</script>

<template>
  <div class="risk-score">
    <h3>Риск провала экзамена</h3>
    <p :style="{ color: riskColor(score) }">
      {{ riskLabel(score) }} ({{ (score * 100).toFixed(0) }}%)
    </p>
  </div>
</template>
