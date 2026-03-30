<script setup lang="ts">
import { AdvancedImage } from "@cloudinary/vue";
import { getAvatar } from "@/cloudinary";

defineProps<{
  imageUrl?: string;
  placeholder?: string;
  width?: number;
  height?: number;
}>();
</script>

<template>
  <div class="rounded-full overflow-hidden bg-gray-800 border border-gray-700 shrink-0">
    <AdvancedImage
      v-if="imageUrl"
      :cld-img="getAvatar(imageUrl, width, height)"
      class="w-full h-full object-cover"
    />
    <div
      v-else
      class="w-full h-full flex items-center justify-center bg-gray-700 text-gray-400 text-xs"
    >
      {{ placeholder || '?' }}
    </div>
  </div>
</template>
