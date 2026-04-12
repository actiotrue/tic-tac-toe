<script lang="ts" setup>
import { computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import AvatarImage from "@/components/AvatarImage.vue";
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue";
import { useSpectatorGame } from "@/composables/useSpectatorGame";
import { GameStatus } from "@/types/game";
import GameBoard from "./GameBoard.vue";
import TurnTimer from "./TurnTimer.vue";

const props = defineProps<{
  gameId: string;
}>();

const router = useRouter();

const {
  game,
  timer,
  players,
  gameStatus,
  error,
  connect,
} = useSpectatorGame(props.gameId);

const firstPlayer = computed(() => players.value.find(player => player.side === "X"));
const secondPlayer = computed(() => players.value.find(player => player.side === "O"));

const statusMessage = computed<string>(() => {
  if (gameStatus.value === GameStatus.Waiting) {
    return "Connecting to game...";
  }

  if (game.winner.value === "draw") {
    return "Draw";
  }

  if (game.winner.value === "X") {
    return `${firstPlayer.value?.username || "Player X"} won`;
  }

  if (game.winner.value === "O") {
    return `${secondPlayer.value?.username || "Player O"} won`;
  }

  if (!game.currentPlayerSymbol.value) {
    return "Live game";
  }

  const current = players.value.find(player => player.side === game.currentPlayerSymbol.value);
  if (!current) {
    return `Turn: ${game.currentPlayerSymbol.value}`;
  }

  return `Turn: ${current.username}`;
});

function goHome() {
  router.push("/");
}

onMounted(() => {
  connect();
});
</script>

<template>
  <div class="flex min-h-[70vh] w-full flex-col items-center justify-center px-0 py-4 sm:min-h-[80vh] sm:px-4">
    <div v-if="error" class="mb-4 rounded-lg bg-red-100 p-4 text-red-500">
      {{ error }}
    </div>

    <div v-if="gameStatus === GameStatus.Waiting" class="flex flex-col items-center gap-4">
      <LoadingSpinner size="lg" />
      <span class="text-gray-400">Connecting to stream...</span>
    </div>

    <div v-else class="w-full">
      <div class="mb-4">
        <TurnTimer v-if="gameStatus === GameStatus.Playing" :seconds="timer.secondsLeft.value" />
        <span v-else class="flex items-center justify-center text-center text-base sm:text-lg">
          Game finished
        </span>
      </div>

      <GameBoard
        :board="game.board.value"
        :current-player="game.currentPlayerSymbol.value"
        :winner="game.winner.value"
        :winning-line="game.winningLine.value ?? []"
        :disabled="true"
        :status-message="statusMessage"
      />

      <div class="mt-6 flex items-center justify-center gap-8 text-sm text-gray-300">
        <div class="flex items-center gap-2">
          <AvatarImage
            :image-url="firstPlayer?.imageUrl"
            :placeholder="firstPlayer?.username?.[0]?.toUpperCase() || 'X'"
            :width="36"
            :height="36"
          />
          <span>{{ firstPlayer?.username || "Player X" }}</span>
        </div>
        <div class="text-xs uppercase tracking-wide text-gray-500">
          vs
        </div>
        <div class="flex items-center gap-2">
          <AvatarImage
            :image-url="secondPlayer?.imageUrl"
            :placeholder="secondPlayer?.username?.[0]?.toUpperCase() || 'O'"
            :width="36"
            :height="36"
          />
          <span>{{ secondPlayer?.username || "Player O" }}</span>
        </div>
      </div>

      <div class="mt-6 flex justify-center">
        <button
          class="rounded-md bg-violet-400 px-4 py-2 text-sm text-white"
          @click="goHome"
        >
          Back to home
        </button>
      </div>
    </div>
  </div>
</template>