<script setup lang="ts">
import { cn } from "@/components/utils";

defineProps<{
  className?: string;
}>();
</script>

<template>
  <h4
    data-slot="card-title"
    :class="cn('leading-none', className)"
  >
    <slot />
  </h4>
</template>
