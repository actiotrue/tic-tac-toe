import type { GameBoard, PlayerSymbol, Winner } from "@/types/game";

const lines: [number, number, number][] = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

export function randomPlayerSymbol(): PlayerSymbol {
  if (Math.random() >= 0.5) {
    return "X";
  }
  return "O";
}

export function calculateWinner(board: GameBoard): { winner: Winner | null; winningLine?: number[] } {
  for (const line of lines) {
    const [a, b, c] = line;
    const s = board[a];
    if (s && s === board[b] && s === board[c]) {
      return { winner: s, winningLine: line };
    }
  }
  return { winner: board.every(cell => cell !== null) ? "draw" : null };
}

export function getAIMove(board: GameBoard, ai: PlayerSymbol, player: PlayerSymbol): number | null {
  const emptyIndices = board
    .map((cell, index) => (cell === null ? index : -1))
    .filter(cell => cell !== -1);
  if (emptyIndices.length === 0) {
    return null;
  }
  let bestMove = findWinningMove(board, ai);
  if (bestMove !== -1) {
    return bestMove;
  }
  bestMove = findWinningMove(board, player);
  if (bestMove === -1) {
    const randomEmptyIndex = emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
    if (randomEmptyIndex !== undefined) {
      bestMove = randomEmptyIndex;
    }
  }
  return bestMove;
}

export function findWinningMove(board: GameBoard, symbol: PlayerSymbol): number {
  for (const line of lines) {
    const [a, b, c] = line;
    const values = [board[a], board[b], board[c]];
    const symbolCount = values.filter(val => val === symbol).length;
    const emptyCount = values.filter(val => val === null).length;
    if (symbolCount === 2 && emptyCount === 1) {
      // if move will be on 0, js will return -1, so we need check for undefined
      const move = line.find(i => board[i] === null);
      return move !== undefined ? move : -1;
    }
  }
  return -1;
}
