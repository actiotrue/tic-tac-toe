<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";

const startTime = Date.now();
const now = ref(Date.now());

let interval: any;

onMounted(() => {
  interval = setInterval(() => {
    now.value = Date.now();
  }, 1000);
});

const secondsTotal = computed(() => Math.floor((now.value - startTime) / 1000));

const formattedTime = computed(() => {
  const mins = Math.floor(secondsTotal.value / 60);
  const secs = secondsTotal.value % 60;
  return `${mins}:${secs.toString().padStart(2, "0")}`;
});

onUnmounted(() => {
  clearInterval(interval);
});
</script>

<template>
  <span>{{ formattedTime }}</span>
</template>
