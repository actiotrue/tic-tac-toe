<script setup lang="ts">
import { cn } from "@/lib/utils";

defineProps<{
  className?: string;
}>();
</script>

<template>
  <div
    data-slot="card-header"
    :class="
      cn(
        'items-start gap-1.5 px-6 pt-6',
        className,
      )
    "
  >
    <slot />
  </div>
</template>
