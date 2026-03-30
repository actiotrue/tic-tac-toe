<script setup lang="ts">
import { cn } from "@/components/utils";

defineProps<{
  className?: string;
}>();
</script>

<template>
  <div
    data-slot="card-header"
    :class="
      cn(
        '@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start gap-1.5 px-6 pt-6 has-data-[slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6',
        className,
      )
    "
  >
    <slot />
  </div>
</template>
