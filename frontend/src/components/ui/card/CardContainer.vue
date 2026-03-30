<script setup lang="ts">
import { cn } from "@/components/utils";

defineProps<{
  className?: string;
}>();
</script>

<template>
  <div
    data-slot="card-container"
    :class="cn('flex flex-col gap-6 rounded-xl border border-custom-transparent', className)"
  >
    <slot />
  </div>
</template>
