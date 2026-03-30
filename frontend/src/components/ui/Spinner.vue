<script setup lang="ts">
import { computed } from "vue";

interface Props {
  size?: "sm" | "md" | "lg" | "xl";
}

const props = withDefaults(defineProps<Props>(), {
  size: "md",
});

const sizeClasses = {
  sm: "w-6 h-6",
  md: "w-10 h-10",
  lg: "w-16 h-16",
  xl: "w-24 h-24",
};

const loaderClass = computed(() => sizeClasses[props.size]);
</script>

<template>
  <span class="loader text-current" :class="[loaderClass]" />
</template>

<style scoped>
.loader {
  display: block;
  position: relative;
  --base-size: 100%;
  animation: rotation 1s linear infinite;
}

.loader::after,
.loader::before {
  content: "";
  box-sizing: border-box;
  position: absolute;
  width: 50%;
  height: 50%;
  top: 50%;
  left: 50%;
  transform: scale(0.5) translate(0, 0);
  background-color: currentColor;
  border-radius: 50%;
  animation: animloader 1s infinite ease-in-out;
}

.loader::before {
  background-color: currentColor;
  opacity: 0.7;
  transform: scale(0.5) translate(-100%, -100%);
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes animloader {
  50% {
    transform: scale(1) translate(-50%, -50%);
  }
}
</style>
