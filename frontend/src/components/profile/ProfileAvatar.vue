<script setup lang="ts">
import { CameraIcon } from "@heroicons/vue/24/outline";
import { ref } from "vue";

import AvatarImage from "../AvatarImage.vue";

const props = defineProps<{
  imageUrl: string;
}>();

const emits = defineEmits<{
  (e: "update", file: File): void;
}>();

const currentImageUrl = ref<string>(props.imageUrl);

const fileInput = ref<HTMLInputElement | null>(null);

function onUpdate(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (!file) {
    return;
  }
  emits("update", file);
}
</script>

<template>
  <div class="relative">
    <input ref="fileInput" type="file" class="hidden" accept="image/*" @change="onUpdate">
    <AvatarImage
      :image-url="currentImageUrl"
      :width="130"
      :height="130"
      class="h-24 w-24 rounded-full border-4 border-gray-600 sm:h-32.5 sm:w-32.5"
    />
    <button
      class="absolute cursor-pointer bottom-2 right-2 bg-purple-600 rounded-full p-2 hover:bg-purple-400"
      type="button"
      @click="fileInput?.click()"
    >
      <CameraIcon class="w-5 h-5" />
    </button>
  </div>
</template>
