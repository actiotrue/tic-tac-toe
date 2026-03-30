<script setup lang="ts">
import { cn } from "@/components/utils";

defineProps<{
  className?: string;
}>();
</script>

<template>
  <div
    data-slot="card-action"
    :class="cn(
      'col-start-2 row-span-2 row-start-1 self-start justify-self-end',
      className,
    )"
  >
    <slot />
  </div>
</template>
