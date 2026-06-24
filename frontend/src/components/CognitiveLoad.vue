<script setup>
defineProps({
  index: {
    type: Number,
    default: 0,
  },
});

function levelLabel(index) {
  if (index < 0.33) return "низкая";
  if (index < 0.66) return "средняя";
  return "высокая";
}
</script>

<template>
  <div class="cognitive-load">
    <h3>Когнитивная нагрузка</h3>
    <div class="bar">
      <div class="bar-fill" :style="{ width: `${index * 100}%` }"></div>
    </div>
    <p>{{ levelLabel(index) }} ({{ (index * 100).toFixed(0) }}%)</p>
  </div>
</template>

<style scoped>
.bar {
  width: 100%;
  height: 12px;
  background: #eee;
  border-radius: 6px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  background: #ff7043;
  transition: width 0.3s ease;
}
</style>
