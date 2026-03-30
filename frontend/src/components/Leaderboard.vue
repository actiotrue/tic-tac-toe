<script setup lang="ts">
import type { RankedPlayer } from "@/types/player";
import AvatarImage from "./AvatarImage.vue";

defineProps<{
  players: RankedPlayer[];
}>();
</script>

<template>
  <div class="w-full overflow-x-auto max-h-65 overflow-y-auto">
    <table class="w-full border-collapse text-left">
      <thead class="top-0 z-10">
        <tr class="border-b border-gray-800 text-gray-400 text-sm uppercase tracking-wider">
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
        <tr v-for="player in players" :key="player.userId" class="transition-colors group">
          <td class="py-2 px-2">
            <span
              class="inline-flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm" :class="[
                player.rank === 1
                  ? 'bg-yellow-300'
                  : player.rank === 2
                    ? 'bg-gray-500'
                    : player.rank === 3
                      ? 'bg-orange-400'
                      : 'bg-gray-300',
              ]"
            >
              {{ player.rank }}
            </span>
          </td>

          <td class="py-2 px-2">
            <div class="flex items-center gap-3">
              <AvatarImage
                :image-url="player.imageUrl"
                :placeholder="player.username.charAt(0).toUpperCase()"
                class="w-10 h-10 rounded-full overflow-hidden bg-gray-800 border border-gray-700"
              />
              <span class="font-semibold group-hover:text-gray-500 transition-colors">
                {{ player.username }}
              </span>
            </div>
          </td>
          <td class="py-2 px-2 text-right font-mono font-bold text-violet-400">
            {{ player.rating }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
