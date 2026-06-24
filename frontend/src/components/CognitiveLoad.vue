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
  <div class="card p-5">
    <h3 class="mb-3 text-sm font-medium text-text/70">Когнитивная нагрузка</h3>
    <div class="h-2 w-full overflow-hidden rounded-full bg-white/10">
      <div
        class="h-full rounded-full bg-gradient-to-r from-accent to-orange-400 transition-all duration-300"
        :style="{ width: `${index * 100}%` }"
      ></div>
    </div>
    <p class="mt-2 text-sm text-text/60">{{ levelLabel(index) }} ({{ (index * 100).toFixed(0) }}%)</p>
  </div>
</template>
