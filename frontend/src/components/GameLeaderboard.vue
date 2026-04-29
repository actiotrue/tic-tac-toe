<script setup lang="ts">
import type { RankedPlayer } from "@/types/player";
import { onMounted, ref } from "vue";
import { getLeaderboard } from "@/api/player";
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue";
import { useProfile } from "@/composables/useProfile";
import GameLeaderboardDesctop from "./GameLeaderboardDesctop.vue";
import GameLeaderboardMobile from "./GameLeaderboardMobile.vue";

const { goToProfile } = useProfile();

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
      <div class="hidden sm:block space-y-3">
        <GameLeaderboardDesctop :players="players" @click-player="goToProfile" />
      </div>
    </div>
    <div class="sm:hidden">
      <GameLeaderboardMobile :players="players" @click-player="goToProfile" />
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
