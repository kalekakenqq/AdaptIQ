<script setup>
defineProps({
  height: {
    type: String,
    default: "h-20",
  },
});
</script>

<template>
  <div :class="['animate-pulse rounded-xl bg-white/5', height]"></div>
</template>
