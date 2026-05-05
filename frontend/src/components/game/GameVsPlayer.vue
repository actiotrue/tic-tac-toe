<script lang="ts" setup>
import { computed, onBeforeUnmount, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useOnlineGame } from "@/composables/useOnlineGame";
import quizData from "../../questions.json";
import { GameStatus } from "../../types/game";
import AvatarImage from "../AvatarImage.vue";
import LoadingSpinner from "../ui/LoadingSpinner.vue";
import GameBoard from "./GameBoard.vue";
import GameResultModal from "./GameResultModal.vue";
import Quiz from "./Quiz.vue";
import SearchingTimer from "./SearchingTimer.vue";
import TurnTimer from "./TurnTimer.vue";
import { getWinnerText } from "./utils";

const {
  game,
  timer,
  me,
  opponent,
  playerSide,
  gameStatus,
  error,
  rematchReady,
  isGameClosed,
  clear,
  handleGame,
  makeMove,
  leaveWaitingQueue,
  sendRematchRequest,
  startNewGame,
} = useOnlineGame();

const router = useRouter();
const isGameOver = computed<boolean>(() => gameStatus.value === GameStatus.Finished);

function handleCellClick(index: number) {
  if (game.currentPlayerSymbol.value !== playerSide.value || game.board.value[index] !== null)
    return;
  makeMove(index);
}

function getStatusClass(userId: string | undefined) {
  if (isGameClosed.value)
    return "bg-red-500";

  const isReady = userId ? rematchReady.value.get(userId) : false;
  return isReady ? "bg-green-500" : "bg-yellow-400 animate-pulse";
}

const isMeReady = computed<boolean>(() => {
  if (!me.value)
    return false;
  return rematchReady.value.get(me.value.userId) === true;
});

const statusMessage = computed<string>(() => {
  if (game.winner.value && playerSide.value) {
    return getWinnerText(game.winner.value, playerSide.value);
  }
  else {
    if (game.currentPlayerSymbol.value === playerSide.value)
      return `Your turn ${game.currentPlayerSymbol.value}`;
    return `Opponent turn ${game.currentPlayerSymbol.value}`;
  }
});

const resultText = computed<string>(() => {
  if (game.winner.value && playerSide.value) {
    return getWinnerText(game.winner.value, playerSide.value);
  }
  return "Wrong result";
});

function handleHome() {
  router.push({ name: "home" });
}

function handleNewGame() {
  clear();
  startNewGame();
}

function handleRematch() {
  sendRematchRequest();
}

onMounted(() => {
  handleGame();
});

onBeforeUnmount(() => {
  if (gameStatus.value === GameStatus.Playing || gameStatus.value === GameStatus.Finished) {
    return;
  }
  leaveWaitingQueue();
});
</script>

<template>
  <div class="flex min-h-[70vh] w-full flex-col items-center justify-center px-0 sm:min-h-[80vh] sm:px-4">
    <div v-if="error" class="p-4 mb-4 text-red-500 bg-red-100 rounded-lg animate-pulse">
      {{ error }}
    </div>
    <div v-if="gameStatus === GameStatus.Waiting" class="flex flex-col items-center gap-4">
      <LoadingSpinner size="lg" />
      <span class="text-gray-400">Connecting to the server...</span>
    </div>
    <div v-else-if="gameStatus === GameStatus.Searching" class="w-full max-w-md space-y-6">
      <div class="flex flex-col items-center p-6 bg-quiz rounded-2xl backdrop-blur-sm">
        <SearchingTimer />
        <p class="mt-2 text-sm text-gray-400">
          Finding a opponent...
        </p>
      </div>
      <Quiz class="bg-quiz" :questions="quizData" />
    </div>
    <div v-else-if="gameStatus === GameStatus.Playing || gameStatus === GameStatus.Finished" class="w-full">
      <div class="mb-4">
        <TurnTimer v-if="gameStatus === GameStatus.Playing" :seconds="timer.secondsLeft.value" />
        <span v-else-if="gameStatus === GameStatus.Finished" class="flex items-center justify-center text-center text-base sm:text-lg">
          Game over
        </span>
      </div>
      <GameBoard
        :board="game.board.value"
        :current-player="game.currentPlayerSymbol.value || 'X'"
        :winner="game.winner.value"
        :winning-line="game.winningLine.value ?? []"
        :disabled="gameStatus === GameStatus.Finished || game.currentPlayerSymbol.value !== playerSide"
        :status-message="statusMessage"
        @cell-click="handleCellClick"
      />
    </div>
    <GameResultModal
      :is-open="isGameOver"
      :result="resultText"
      :is-rematch="isMeReady || isGameClosed"
      @rematch="handleRematch"
      @new-game="handleNewGame"
      @home="handleHome"
    >
      <template #player-left>
        <div class="flex flex-col items-center space-y-2 text-white">
          <AvatarImage :image-url="me?.imageUrl" :placeholder="me?.username?.toUpperCase() || '?'" :width="80" :height="80" />
          <p>{{ me?.username }}</p>
          <div
            class="absolute -top-1 -right-1 w-4 h-4 rounded-full border-2 border-slate-800"
            :class="getStatusClass(me?.userId)"
          />
        </div>
      </template>

      <template #player-right>
        <div class="flex flex-col items-center space-y-2 text-white">
          <AvatarImage :image-url="opponent?.imageUrl" :placeholder="opponent?.username?.toUpperCase() || '?'" :width="80" :height="80" />
          <p>{{ opponent?.username }}</p>
          <div
            class="absolute -top-1 -right-1 w-4 h-4 rounded-full border-2 border-slate-800"
            :class="getStatusClass(opponent?.userId)"
          />
        </div>
      </template>
    </GameResultModal>
  </div>
</template>

<style scoped>
.timer-background {
  background: #2a2a2a;
}
</style>
