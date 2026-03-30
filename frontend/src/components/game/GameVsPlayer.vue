<script lang="ts" setup>
import { computed, onBeforeUnmount, onMounted } from "vue";
import { useMatchmaking } from "@/composables/useMatchmaking";
import { GameStatus } from "../../types/game";
import Spinner from "../ui/Spinner.vue";
import GameBoard from "./GameBoard.vue";
import SearchingTimer from "./SearchingTimer.vue";

const {
  board,
  currentPlayer,
  playerSide,
  winner,
  winningLine,
  gameStatus,
  error,
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
  <div class="">
    <div v-if="error" class="text-lg text-red-500">
      {{ error }}
    </div>
    <div v-else-if="gameStatus === GameStatus.Waiting" class="flex items-center justify-center">
      <Spinner size="lg" />
    </div>
    <div v-else-if="gameStatus === GameStatus.Searching" class="flex items-center justify-center">
      <SearchingTimer />
    </div>
    <div v-else-if="gameStatus === GameStatus.Playing || gameStatus === GameStatus.Finished">
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
