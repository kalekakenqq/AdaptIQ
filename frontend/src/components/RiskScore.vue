<script setup>
defineProps({
  score: {
    type: Number,
    default: 0,
  },
});

function riskLabel(score) {
  if (score < 0.33) return "Низкий риск";
  if (score < 0.66) return "Средний риск";
  return "Высокий риск";
}

function badgeClass(score) {
  if (score < 0.33) return "bg-green-500/15 text-green-400";
  if (score < 0.66) return "bg-yellow-500/15 text-yellow-400";
  return "bg-red-500/15 text-red-400";
}
</script>

<template>
  <div class="card p-5">
    <h3 class="mb-3 text-sm font-medium text-text/70">Риск провала экзамена</h3>
    <span :class="['inline-block rounded-full px-3 py-1 text-sm font-medium', badgeClass(score)]">
      {{ riskLabel(score) }} · {{ (score * 100).toFixed(0) }}%
    </span>
  </div>
</template>
