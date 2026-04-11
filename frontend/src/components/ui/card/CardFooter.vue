<script setup lang="ts">
import { cn } from "@/lib/utils";

defineProps<{
  className?: string;
}>();
</script>

<template>
  <div
    data-slot="card-footer"
    :class="cn('flex items-center px-6 pb-6 [.border-t]:pt-6', className)"
  >
    <slot />
  </div>
</template>
