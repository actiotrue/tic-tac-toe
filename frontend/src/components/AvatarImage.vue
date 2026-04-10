<script setup lang="ts">
import { AdvancedImage } from "@cloudinary/vue";
import { computed } from "vue";
import { getAvatar } from "@/cloudinary";

const props = withDefaults(defineProps<{
  imageUrl?: string;
  placeholder?: string;
  width?: number;
  height?: number;
}>(), {
  width: 40,
  height: 40,
});

const containerStyle = computed(() => ({
  width: `${props.width}px`,
  height: `${props.height}px`,
}));
</script>

<template>
  <div
    class="rounded-full overflow-hidden bg-gray-800 border border-gray-700 shrink-0"
    :style="containerStyle"
  >
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
