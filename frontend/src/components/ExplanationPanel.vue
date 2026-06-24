<script setup>
defineProps({
  explanation: {
    type: Object,
    default: () => ({}),
  },
});
</script>

<template>
  <div class="explanation-panel">
    <h3>Почему система приняла такое решение</h3>
    <ul>
      <li v-for="(value, feature) in explanation" :key="feature">
        <strong>{{ feature }}</strong>: {{ value.toFixed(3) }}
      </li>
    </ul>
    <p v-if="Object.keys(explanation).length === 0">Объяснение пока недоступно.</p>
  </div>
</template>
