import { computed, ref } from "vue";

import type { Cell, GameBoard, PlayerSymbol, Winner } from "@/types/game";

import { calculateWinner } from "@/components/game/utils";

export function useTicTacToe() {
  const board = ref<GameBoard>(Array.from<Cell>({ length: 9 }).fill(null));
  const currentPlayer = ref<PlayerSymbol>("X");

  const startTime = ref<number | null>(null);
  const endTime = ref<number | null>(null);

  const result = computed<{ winner: Winner | null; winningLine?: number[] }>(() => {
    const gameResult = calculateWinner(board.value);
    if (gameResult.winner) {
      endTime.value = Date.now();
    }
    return gameResult;
  });

  const makeMove = (index: number) => {
    if (result.value.winner || board.value[index])
      return;

    if (board.value.every(cell => cell === null)) {
      startTime.value = Date.now();
    }

    board.value[index] = currentPlayer.value;
    currentPlayer.value = currentPlayer.value === "X" ? "O" : "X";
  };

  const reset = (newPlayerSymbol: PlayerSymbol = "X") => {
    board.value = Array.from<Cell>({ length: 9 }).fill(null);
    currentPlayer.value = newPlayerSymbol;
  };

  const durationInSeconds = computed(() => {
    if (!startTime.value || !endTime.value)
      return 0;
    return Math.floor((endTime.value - startTime.value) / 1000);
  });

  return { board, currentPlayer, durationInSeconds, result, makeMove, reset };
}
