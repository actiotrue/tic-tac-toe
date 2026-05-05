<script setup lang="ts">
import type { Player } from "@/types/player";
import AvatarImage from "./AvatarImage.vue";

defineProps<{
  players: Player[];
}>();

const emit = defineEmits<{
  clickPlayer: [playerId: string];
}>();
</script>

<template>
  <div
    v-for="player in $props.players"
    :key="player.userId"
    class="flex items-center justify-between p-3 rounded-xl"
  >
    <div class="flex items-center gap-3 min-w-0">
      <span
        class="flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm shrink-0"
        :class="[
          player.rank === 1 ? 'bg-yellow-300 text-white'
          : player.rank === 2 ? 'bg-gray-400 text-white'
            : player.rank === 3 ? 'bg-orange-400 text-white'
              : 'bg-gray-500 text-white',
        ]"
      >
        {{ player.rank }}
      </span>

      <div
        class="flex items-center gap-2 min-w-0"
        @click="emit('clickPlayer', player.userId)"
      >
        <AvatarImage
          :image-url="player.imageUrl"
          :placeholder="player.username.charAt(0).toUpperCase()"
          class="cursor-pointer w-8 h-8 rounded-full bg-gray-800 border border-gray-700"
        />
        <span class="truncate font-semibold">
          {{ player.username }}
        </span>
      </div>
    </div>

    <div class="text-sm font-mono font-bold text-violet-400">
      {{ player.rating }}
    </div>
  </div>
</template>
