<script setup>
import { RouterView } from "vue-router";

import Notification from "./components/Notification.vue";
import Onboarding from "./components/Onboarding.vue";
</script>

<template>
  <RouterView />
  <Notification />
  <Onboarding />
</template>
