<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const videoRef = ref(null);
const wsConnection = ref(null);
const cognitiveLoadIndex = ref(0);

const props = defineProps({
  sessionId: {
    type: String,
    required: true,
  },
  wsBaseUrl: {
    type: String,
    default: () =>
      import.meta.env.VITE_WS_BASE_URL ||
      `${window.location.protocol === "https:" ? "wss:" : "ws:"}//${window.location.host}`,
  },
});

const emit = defineEmits(["cognitive-load-update"]);

async function startCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  videoRef.value.srcObject = stream;
}

function connectWebSocket() {
  wsConnection.value = new WebSocket(`${props.wsBaseUrl}/ws/session/${props.sessionId}`);
  wsConnection.value.onmessage = (event) => {
    const payload = JSON.parse(event.data);
    cognitiveLoadIndex.value = payload.cognitive_load_index;
    emit("cognitive-load-update", cognitiveLoadIndex.value);
  };
}

onMounted(async () => {
  await startCamera();
  connectWebSocket();
});

onBeforeUnmount(() => {
  wsConnection.value?.close();
});
</script>

<template>
  <div class="camera-widget">
    <video ref="videoRef" autoplay muted playsinline width="320" height="240" />
  </div>
</template>
