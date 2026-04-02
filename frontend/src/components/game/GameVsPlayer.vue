<script lang="ts" setup>
import { computed, onBeforeUnmount, onMounted } from "vue";
import { useMatchmaking } from "@/composables/useMatchmaking";
import quizData from "../../questions.json";
import { GameStatus } from "../../types/game";
import Spinner from "../ui/Spinner.vue";
import GameBoard from "./GameBoard.vue";
import Quiz from "./Quiz.vue";
import SearchingTimer from "./SearchingTimer.vue";
import TurnTimer from "./TurnTimer.vue";

const {
  board,
  currentPlayer,
  playerSide,
  winner,
  winningLine,
  gameStatus,
  error,
  secondsLeft,
  handleGame,
  makeMove,
  leaveGame,
} = useMatchmaking();

function handleCellClick(index: number) {
  if (currentPlayer.value !== playerSide.value)
    return;
  makeMove(index);
}

const statusMessage = computed(() => {
  if (!winner.value) {
    if (currentPlayer.value === playerSide.value)
      return `Your turn (${currentPlayer.value})`;
    return `Opponent turn (${currentPlayer.value})`;
  }
  return winner.value === "draw"
    ? "Draw"
    : winner.value === playerSide.value
      ? "You win! 🎉"
      : "You lose! 😭";
});

onMounted(() => {
  handleGame();
});

onBeforeUnmount(() => {
  leaveGame();
});
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[80vh] p-4">
    <div v-if="error" class="p-4 mb-4 text-red-500 bg-red-100 rounded-lg animate-pulse">
      {{ error }}
    </div>
    <div v-if="gameStatus === GameStatus.Waiting" class="flex flex-col items-center gap-4">
      <Spinner size="lg" />
      <span class="text-gray-400">Подключение к серверу...</span>
    </div>
    <div v-else-if="gameStatus === GameStatus.Searching" class="w-full max-w-md space-y-6">
      <div class="flex flex-col items-center p-6 timer-background rounded-2xl backdrop-blur-sm">
        <SearchingTimer />
        <p class="mt-2 text-sm text-gray-400">
          Ищем соперника...
        </p>
      </div>
      <Quiz :questions="quizData" />
    </div>
    <div v-else-if="gameStatus === GameStatus.Playing || gameStatus === GameStatus.Finished" class="w-full">
      <div class="mb-4">
        <TurnTimer v-if="gameStatus === GameStatus.Playing" :seconds="secondsLeft" />
        <span v-if="gameStatus === GameStatus.Finished" class="flex items-center justify-center text-lg">
          Игра окончена
        </span>
      </div>
      <GameBoard
        :board="board"
        :current-player="currentPlayer"
        :winner="winner"
        :winning-line="winningLine ?? []"
        :disabled="gameStatus === GameStatus.Finished || currentPlayer !== playerSide"
        :status-message="statusMessage"
        @cell-click="handleCellClick"
      />
    </div>
  </div>
</template>

<style scoped>
.timer-background {
  background: #2a2a2a;
}
</style>
