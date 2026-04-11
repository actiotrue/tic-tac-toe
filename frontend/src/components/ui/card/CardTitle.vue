<script setup lang="ts">
import { cn } from "@/lib/utils";

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
