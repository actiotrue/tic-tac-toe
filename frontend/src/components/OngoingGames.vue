<script lang="ts" setup>
import { computed, onBeforeUnmount, onMounted } from "vue";
import { useRouter } from "vue-router";
import AvatarImage from "@/components/AvatarImage.vue";
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue";
import { useOngoingGames } from "@/composables/useOngoingGames";

const router = useRouter();

const {
  games,
  isLoading,
  error,
  connect,
  disconnect,
} = useOngoingGames();

const hasGames = computed<boolean>(() => games.value.length > 0);

function watchGame(gameId: string) {
  router.push({
    path: "/game",
    query: {
      mode: "spectate",
      gameId,
    },
  });
}

function formatStartTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "just started";
  }
  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

onMounted(() => {
  connect();
});

onBeforeUnmount(() => {
  disconnect();
});
</script>

<template>
  <div class="space-y-3">
    <div v-if="isLoading" class="flex items-center justify-center py-4">
      <LoadingSpinner size="sm" />
    </div>

    <div v-else-if="error" class="space-y-3 rounded-md border border-red-500/20 bg-red-500/10 p-3">
      <p class="text-sm text-red-200">
        {{ error }}
      </p>
      <button
        class="w-full rounded-md bg-violet-400 px-3 py-2 text-sm text-white"
        @click="connect"
      >
        Retry
      </button>
    </div>

    <div v-else-if="!hasGames" class="rounded-md border border-white/10 bg-black/20 p-3 text-sm text-gray-400">
      No active games right now.
    </div>

    <div v-else class="space-y-2">
      <button
        v-for="game in games"
        :key="game.gameId"
        class="flex w-full items-center justify-between gap-3 rounded-md border border-white/10 bg-white/5 px-3 py-2 text-left transition hover:bg-white/10"
        @click="watchGame(game.gameId)"
      >
        <div class="min-w-0">
          <div class="mb-1 flex items-center gap-2">
            <AvatarImage
              :image-url="game.players[0]?.imageUrl"
              :placeholder="game.players[0]?.username?.[0]?.toUpperCase() || 'X'"
              :width="24"
              :height="24"
            />
            <AvatarImage
              :image-url="game.players[1]?.imageUrl"
              :placeholder="game.players[1]?.username?.[0]?.toUpperCase() || 'O'"
              :width="24"
              :height="24"
            />
            <span class="truncate text-sm font-medium text-white">
              {{ game.players[0]?.username || "Player X" }} vs {{ game.players[1]?.username || "Player O" }}
            </span>
          </div>
          <p class="truncate text-xs text-gray-400">
            Turn: {{ game.turn }} • Started at {{ formatStartTime(game.startedAt) }}
          </p>
        </div>
        <span class="shrink-0 text-xs font-medium uppercase tracking-wide text-violet-200">
          Watch
        </span>
      </button>
    </div>
  </div>
</template>