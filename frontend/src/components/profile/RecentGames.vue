<script lang="ts" setup>
import type { GameDetails } from "@/types/game";
import { computed, onMounted, onUnmounted, ref } from "vue";
import { toast } from "vue3-toastify";
import { getRecentGames } from "@/api/player";
import { useAuth } from "@/store/auth.store";
import { getErrorMessage } from "@/utils";
import AvatarImage from "../AvatarImage.vue";
import LoadingSpinner from "../ui/LoadingSpinner.vue";
import { getWinnerText } from "./utils";

const games = ref<GameDetails[]>([]);
const limit = 10;
const offset = ref<number>(0);
const isLoading = ref(false);
const allLoaded = ref(false);

const { userId } = useAuth();

const loadMoreTrigger = ref<HTMLElement | null>(null);
let observer: IntersectionObserver | null = null;

async function loadGames() {
  if (isLoading.value || allLoaded.value)
    return;

  isLoading.value = true;
  try {
    const newGames = await getRecentGames(limit, offset.value);

    if (newGames.length < limit) {
      allLoaded.value = true;
    }

    games.value.push(...newGames);
    offset.value += limit;
  }
  catch (error) {
    toast.error(getErrorMessage(error));
  }
  finally {
    isLoading.value = false;
  }
}

const gamesWithPlayers = computed(() => {
  return games.value.map(game => ({
    ...game,
    playerX: game.players.find(p => p.side === "X"),
    playerO: game.players.find(p => p.side === "O"),
  }));
});

function getRowClass(game: GameDetails) {
  const userSide = game.players.find(p => p.playerId === userId)?.side;
  if (game.result === "draw") {
    return "bg-yellow-500 border-l-4 border-gray-500";
  }
  if ((userSide === "X" && game.result === "x_won") || (userSide === "O" && game.result === "o_won")) {
    return "bg-green-500 border-l-4 border-green-500";
  }
  return "bg-red-500 border-l-4 border-red-500";
}

onMounted(() => {
  observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting && !isLoading.value) {
      loadGames();
    }
  }, {
    rootMargin: "100px",
  });

  if (loadMoreTrigger.value) {
    observer.observe(loadMoreTrigger.value);
  }
});

onUnmounted(() => {
  if (observer)
    observer.disconnect();
});
</script>

<template>
  <div class="w-full">
    <div class="rounded-lg shadow-lg overflow-hidden flex flex-col h-100">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-separate border-spacing-0">
          <thead class="bg-gray-600 text-gray-300 uppercase text-xs font-semibold">
            <tr>
              <th class="px-4 py-3">
                Player X
              </th>
              <th class="px-4 py-3">
                Player O
              </th>
              <th class="px-4 py-3">
                Result
              </th>
              <th class="px-4 py-3 text-right">
                Duration
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-700">
            <tr v-if="games.length === 0">
              <td colspan="4" class="px-4 py-10 text-center text-gray-500">
                Нет недавних игр
              </td>
            </tr>

            <tr
              v-for="game in gamesWithPlayers"
              :key="game.id"
              class="transition-colors duration-200" :class="[getRowClass(game)]"
            >
              <td class="px-4 py-3 font-medium text-gray-200">
                <div class="flex items-center gap-3">
                  <AvatarImage
                    :image-url="game.playerX?.player?.imageUrl"
                    :placeholder="game.playerX?.player?.username?.toUpperCase() || '?'"
                    class="rounded-full overflow-hidden bg-gray-800 border border-gray-700 shrink-0"
                  />
                  <span class="truncate">{{ game.playerX?.player?.username || '—' }}</span>
                </div>
              </td>

              <td class="px-4 py-3 font-medium text-gray-200">
                <div class="flex items-center gap-3">
                  <AvatarImage
                    :image-url="game.playerO?.player?.imageUrl"
                    :placeholder="game.playerO?.player?.username?.toUpperCase() || '?'"
                    :width="40"
                    :height="40"
                    class="w-10 h-10 rounded-full overflow-hidden bg-gray-800 border border-gray-700 shrink-0"
                  />
                  <span class="truncate">{{ game.playerO?.player?.username || '—' }}</span>
                </div>
              </td>

              <td class="px-4 py-3">
                <span
                  class="px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider bg-black/20 text-white"
                >
                  {{ getWinnerText(game.result) }}
                </span>
              </td>
              <td class="px-4 py-3 text-right text-white tabular-nums">
                {{ game.duration }}с
              </td>
            </tr>
          </tbody>
        </table>
        <div
          ref="loadMoreTrigger"
          class="w-full py-4 flex justify-center items-center text-sm text-gray-400"
        >
          <LoadingSpinner v-if="isLoading" size="sm" />
        </div>
      </div>
    </div>
  </div>
</template>
