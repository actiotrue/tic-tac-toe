<script setup lang="ts">
import { cn } from "@/components/utils";

defineProps<{
  className?: string;
}>();
</script>

<template>
  <div
    data-slot="card-content"
    :class="cn('px-6 last:pb-6', className)"
  >
    <slot />
  </div>
</template>
