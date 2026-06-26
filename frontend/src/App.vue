<script setup>
import { onMounted } from "vue";
import { RouterView } from "vue-router";

import Notification from "./components/Notification.vue";
import Onboarding from "./components/Onboarding.vue";
import { useThemeStore } from "./stores/theme";

const themeStore = useThemeStore();

onMounted(() => {
  themeStore.init();
});
</script>

<template>
  <RouterView />
  <Notification />
  <Onboarding />
</template>
