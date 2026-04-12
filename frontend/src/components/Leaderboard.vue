<script setup lang="ts">
import type { RankedPlayer } from "@/types/player";

import { onMounted, ref } from "vue";
import { getLeaderboard } from "@/api/player";
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue";
import AvatarImage from "./AvatarImage.vue";

const limit = 3;

const players = ref<RankedPlayer[]>([]);
const isLoading = ref(false);
const allLoaded = ref(false);
const start = ref(0);
const end = ref(limit);

async function loadPlayers() {
  if (isLoading.value || allLoaded.value)
    return;

  isLoading.value = true;
  try {
    const newPlayers = await getLeaderboard(start.value, end.value);

    if (newPlayers.length < (end.value - start.value)) {
      allLoaded.value = true;
    }

    players.value.push(...newPlayers);
    start.value = start.value + limit;
    end.value = end.value + limit;
  }
  catch {
    players.value = [];
  }
  finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  loadPlayers();
});
</script>

<template>
  <div class="w-full space-y-4">
    <div class="max-h-80 overflow-auto">
      <div class="sm:hidden space-y-3">
        <div
          v-for="player in players"
          :key="player.userId"
          class="flex items-center justify-between p-3 rounded-xl bg-gray-800/40"
        >
          <div class="flex items-center gap-3 min-w-0">
            <span
              class="flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm shrink-0"
              :class="[
                player.rank === 1 ? 'bg-yellow-300 text-black'
                : player.rank === 2 ? 'bg-gray-500 text-black'
                  : player.rank === 3 ? 'bg-orange-400 text-black'
                    : 'bg-gray-600 text-white',
              ]"
            >
              {{ player.rank }}
            </span>

            <div class="flex items-center gap-2 min-w-0">
              <AvatarImage
                :image-url="player.imageUrl"
                :placeholder="player.username.charAt(0).toUpperCase()"
                class="w-8 h-8 rounded-full bg-gray-800 border border-gray-700"
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
      </div>
      <table class="hidden sm:table w-full min-w-[24rem] border-collapse text-left">
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
                class="inline-flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm text-black"
                :class="[
                  player.rank === 1 ? 'bg-yellow-300'
                  : player.rank === 2 ? 'bg-gray-400'
                    : player.rank === 3 ? 'bg-orange-400' : 'bg-gray-600 text-white',
                ]"
              >
                {{ player.rank }}
              </span>
            </td>

            <td class="py-2 px-2">
              <div class="flex min-w-0 items-center gap-3">
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
    </div>

    <div class="flex justify-center pt-2">
      <button
        v-if="!allLoaded"
        :disabled="isLoading"
        class="text-sm font-medium text-violet-700 hover:text-violet-300 disabled:opacity-50 flex items-center gap-2 transition-all"
        @click="loadPlayers"
      >
        <LoadingSpinner v-if="isLoading" size="sm" />
        <span v-if="!isLoading">Load More Players</span>
        <span v-else>Loading...</span>
      </button>
    </div>
  </div>
</template>
