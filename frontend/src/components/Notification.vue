<script setup>
import { useNotificationStore } from "../stores/notifications";

const store = useNotificationStore();

function toneClass(type) {
  if (type === "error") return "border-red-500/40 bg-red-500/10 text-red-200";
  if (type === "warning") return "border-yellow-500/40 bg-yellow-500/10 text-yellow-100";
  return "border-accent/40 bg-accent/10 text-text";
}
</script>

<template>
  <div class="pointer-events-none fixed right-4 top-4 z-50 flex w-80 flex-col gap-2">
    <transition-group name="toast">
      <div
        v-for="item in store.items"
        :key="item.id"
        :class="[
          'pointer-events-auto rounded-xl border px-4 py-3 text-sm shadow-lg backdrop-blur',
          toneClass(item.type),
        ]"
      >
        {{ item.message }}
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(40px);
}
</style>
