<script setup lang="ts">
import { cn } from "@/lib/utils";

defineProps<{
  className?: string;
}>();
</script>

<template>
  <div
    data-slot="card-container"
    :class="cn(
      'flex flex-col gap-4 p-4 rounded-xl border border-custom-transparent',
      'md:gap-6 md:p-6',
      'lg:p-8',
      className,
    )"
  >
    <slot />
  </div>
</template>
