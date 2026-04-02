<script setup lang="ts">
defineProps<{
  seconds: number;
}>();
</script>

<template>
  <div class="flex items-center justify-center">
    <div class="text-2xl font-bold">
      {{ seconds }}
    </div>
    <span class="text-xs font-bold ml-1">
      seconds
    </span>
  </div>
</template>
