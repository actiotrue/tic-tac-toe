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
  <table class="w-full min-w-[24rem] border-collapse text-left">
    <thead class="sticky top-0 z-10">
      <tr class="border-b border-gray-800 text-sm uppercase tracking-wider">
        <th class="py-2 px-2 font-medium w-16">
          Rank
        </th>
        <th class="py-2 px-2 font-medium">
          Player
        </th>
        <th class="py-2 px-2 font-medium text-right">
          Rating
        </th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-800/50">
      <tr v-for="player in players" :key="player.userId" class="transition-colors group hover:bg-white/5">
        <td class="py-2 px-2">
          <span
            class="inline-flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm"
            :class="[
              player.rank === 1 ? 'bg-yellow-300 text-white'
              : player.rank === 2 ? 'bg-gray-400 text-white'
                : player.rank === 3 ? 'bg-orange-400 text-white' : 'bg-gray-600 text-white',
            ]"
          >
            {{ player.rank }}
          </span>
        </td>

        <td class="py-2 px-2">
          <div class="cursor-pointer flex min-w-0 items-center gap-3" @click="emit('clickPlayer', player.userId)">
            <AvatarImage
              :image-url="player.imageUrl"
              :placeholder="player.username.charAt(0).toUpperCase()"
              class="w-10 h-10 rounded-full overflow-hidden bg-gray-800 border border-gray-700"
            />
            <span class="truncate font-semibold transition-colors group-hover:text-violet-400">
              {{ player.username }}
            </span>
          </div>
        </td>
        <td class="py-2 px-2 text-right font-mono font-bold text-violet-700 whitespace-nowrap">
          {{ player.rating }}
        </td>
      </tr>
    </tbody>
  </table>
</template>
