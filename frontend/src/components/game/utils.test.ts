import { afterEach, describe, expect, it, vi } from "vitest";

import type { GameBoard, PlayerSymbol, Winner } from "../../types/game";

import { calculateWinner, findWinningMove, getAIMove } from "./utils";

// You can declare board like:  `. . .
//                              X O X
//                              . . .`
function b(str: string): GameBoard {
  const cells = str
    .trim()
    .split(/\s+/)
    .map((cell) => {
      if (cell === "." || cell === "_" || cell.toLowerCase() === "null")
        return null;
      return cell as PlayerSymbol;
    });

  if (cells.length !== 9) {
    throw new Error(`Board must have 9 cells, but got ${cells.length}`);
  }

  return cells as GameBoard;
}

// ======== findWinningMove ========
type TestCaseWinningMove = {
  name: string;
  board: GameBoard;
  symbol: PlayerSymbol;
  expected: number;
};

const casesWinningMove: TestCaseWinningMove[] = [
  {
    name: "returns winning move when two symbols and one empty in a row",
    board: b(`X X .
              . . . 
              . . .`),
    symbol: "X",
    expected: 2,
  },
  {
    name: "returns winning move for column",
    board: b(`O . .
              O . . 
              . . .`),
    symbol: "O",
    expected: 6,
  },
  {
    name: "returns winning move for diagonal",
    board: b(`X . .
              . X . 
              . . .`),
    symbol: "X",
    expected: 8,
  },
  {
    name: "returns -1 when there is no winning move",
    board: b(`X O X
              X O O
              O X X`),
    symbol: "X",
    expected: -1,
  },
  {
    name: "returns -1 when only one symbol in line",
    board: b(`X . .
              . . .
              . . .`),
    symbol: "X",
    expected: -1,
  },
  {
    name: "does not confuse opponent symbols",
    board: b(`X X . 
              . . . 
              . . .`),
    symbol: "O",
    expected: -1,
  },
];

describe("findWinningMove (table-driven)", () => {
  it.each(casesWinningMove)("$name", ({ board, symbol, expected }) => {
    expect(findWinningMove(board, symbol)).toBe(expected);
  });
});

// ======== calculateWinner ========
type TestCaseCalculateWinner = {
  name: string;
  board: GameBoard;
  expected: { winner: Winner | null; winningLine?: number[] };
};

const casesCalculateWinner: TestCaseCalculateWinner[] = [
  {
    name: "X wins by row",
    board: b(`X X X 
              . . . 
              . . .`),
    expected: { winner: "X", winningLine: [0, 1, 2] },
  },
  {
    name: "O wins by column",
    board: b(`O . . 
              O . . 
              O . .`),
    expected: { winner: "O", winningLine: [0, 3, 6] },
  },
  {
    name: "X wins by diagonal",
    board: b(`X . .
              . X . 
              . . X`),
    expected: { winner: "X", winningLine: [0, 4, 8] },
  },
  {
    name: "Draw when board is full and no winner",
    board: b(`X O X 
              X O O 
              O X X`),
    expected: { winner: "Draw" },
  },
  {
    name: "Game in progress returns null",
    board: b(`X O .
              . X . 
              . . .`),
    expected: { winner: null },
  },
  {
    name: "Winner has priority over Draw on full board",
    board: b(`O O O 
              X X O 
              X O X`),
    expected: { winner: "O", winningLine: [0, 1, 2] },
  },
];

describe("calculateWinner (table-driven)", () => {
  it.each(casesCalculateWinner)("$name", ({ board, expected }) => {
    expect(calculateWinner(board)).toStrictEqual(expected);
  });
});

// ======== getAIMove ========
vi.spyOn(Math, "random").mockReturnValue(0);

type TestCaseAIMove = {
  name: string;
  board: GameBoard;
  ai: PlayerSymbol;
  player: PlayerSymbol;
  expected: number | null;
  mockRandom?: number;
};

const casesAIMove: TestCaseAIMove[] = [
  {
    name: "returns winning move for AI",
    board: b(`O O . 
              . . . 
              . . .`),
    ai: "O",
    player: "X",
    expected: 2,
  },
  {
    name: "blocks player winning move",
    board: b(`X X . 
              . . . 
              . . .`),
    ai: "O",
    player: "X",
    expected: 2,
  },
  {
    name: "returns random empty cell when no win or block",
    board: b(`X . . 
              . O . 
              . . .`),
    ai: "O",
    player: "X",
    mockRandom: 0,
    expected: 1,
  },
  {
    name: "returns null when board is full",
    board: b(`X O X 
              X O O
              O X X`),
    ai: "O",
    player: "X",
    expected: null,
  },
];

describe("getAIMove (table-driven)", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it.each(casesAIMove)("$name", ({ board, ai, player, expected, mockRandom }) => {
    if (mockRandom !== undefined) {
      vi.spyOn(Math, "random").mockReturnValue(mockRandom);
    }

    expect(getAIMove(board, ai, player)).toBe(expected);
  });
});
