<script setup lang="ts">
import { cn } from "@/components/utils";

defineProps<{
  className?: string;
}>();
</script>

<template>
  <p
    data-slot="card-description"
    :class="cn('', className)"
  >
    <slot />
  </p>
</template>
