import { ref } from "vue";

import type { Cell, GameBoard, PlayerSymbol, Winner } from "@/types/game";

type newGameState = {
  board: GameBoard;
  currentPlayerSymbol: PlayerSymbol;
  winner: Winner | null;
  winningLine: number[] | null;
};

export function useGameState() {
  const board = ref<GameBoard>(Array.from<Cell>({ length: 9 }).fill(null));
  const currentPlayerSymbol = ref<PlayerSymbol | null>(null);
  const winner = ref<Winner | null>(null);
  const winningLine = ref<number[] | null>(null);

  const makeMove = (index: number) => {
    if (winner.value || board.value[index])
      return;

    board.value[index] = currentPlayerSymbol.value;
  };

  const setState = (newState: Partial<newGameState>) => {
    if (newState.board !== undefined)
      board.value = newState.board;
    if (newState.currentPlayerSymbol !== undefined)
      currentPlayerSymbol.value = newState.currentPlayerSymbol;
    if (newState.winner !== undefined)
      winner.value = newState.winner;
    if (newState.winningLine !== undefined)
      winningLine.value = newState.winningLine;
  };

  const reset = () => {
    board.value = Array.from<Cell>({ length: 9 }).fill(null);
    currentPlayerSymbol.value = null;
    winner.value = null;
    winningLine.value = null;
  };

  return { board, currentPlayerSymbol, winner, winningLine, makeMove, setState, reset };
}
