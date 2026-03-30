<script lang="ts" setup>
import type { PlayerSymbol } from "../../types/game";
import { uuidv7 } from "uuidv7";
import { computed, onMounted, ref, watch } from "vue";
import { createGame } from "@/api/game";
import { useTicTacToe } from "@/composables/useTicTacToe";
import { useAuth } from "@/store/auth.store";
import GameBoard from "./GameBoard.vue";
import { getAIMove, randomPlayerSymbol } from "./utils";

const playerSymbol = ref<PlayerSymbol>(randomPlayerSymbol());
const aiSymbol = computed(() => (playerSymbol.value === "X" ? "O" : "X"));

const { userId } = useAuth();

const { board, currentPlayer, durationInSeconds, result, makeMove, reset } = useTicTacToe();

function handleCellClick(index: number) {
  if (currentPlayer.value !== playerSymbol.value)
    return;
  makeMove(index);
}

watch(currentPlayer, (player) => {
  if (player !== aiSymbol.value)
    return;
  if (result.value.winner)
    return;

  setTimeout(() => {
    const aiMove = getAIMove(board.value, aiSymbol.value, playerSymbol.value);
    if (aiMove !== null) {
      makeMove(aiMove);
    }
  }, 500);
});

watch(
  () => result.value.winner,
  async (winner) => {
    if (!winner)
      return;
    const gameResult = winner === "draw" ? "draw" : winner === "X" ? "x_won" : "o_won";
    const isPlayerX = playerSymbol.value === "X";
    const gameId = uuidv7();
    try {
      await createGame({
        id: gameId,
        result: gameResult,
        duration: durationInSeconds.value,
        players: [
          {
            gameId,
            playerId: userId,
            side: isPlayerX ? "X" : "O",
            type: "human",
          },
          {
            gameId,
            playerId: null,
            side: isPlayerX ? "O" : "X",
            type: "ai",
          },
        ],
      });
    }
    catch (error) {
      console.error("Failed to save game:", error);
    }
  },
);

function resetGame() {
  const newPlayerSymbol = randomPlayerSymbol();
  playerSymbol.value = newPlayerSymbol;
  reset(newPlayerSymbol);
}

const statusMessage = computed(() => {
  if (!result.value.winner) {
    return currentPlayer.value !== aiSymbol.value
      ? `Your turn (${currentPlayer.value})`
      : `AI turn... (${currentPlayer.value})`;
  }
  if (result.value.winner === "draw")
    return "Draw";
  return result.value.winner === playerSymbol.value ? "You win! 🎉" : "AI win!";
});

onMounted(() => {
  reset(playerSymbol.value);
});
</script>

<template>
  <GameBoard
    :board="board"
    :current-player="currentPlayer"
    :disabled="currentPlayer === aiSymbol"
    :winner="result.winner"
    :winning-line="result.winningLine"
    :status-message="statusMessage"
    @cell-click="handleCellClick"
  >
    <template #footer>
      <button
        class="flex items-center justify-center gap-2 text-white bg-violet-400 w-full rounded-md py-3 transition-all disabled:opacity-50 disabled:cursor-not-allowed enabled:cursor-pointer enabled:hover:bg-violet-500 enabled:hover:opacity-90"
        :disabled="result.winner === null"
        @click="resetGame"
      >
        <ArrowPathIcon class="w-6 h-6" />
        New game
      </button>
    </template>
  </GameBoard>
</template>
