import type { GamePlayerCreate, GameResult, PlayerSummary } from "./shared";

export type PlayerSymbol = "X" | "O";
export type Cell = PlayerSymbol | null;
export type Winner = PlayerSymbol | "draw";
export type GameBoard = Cell[];

export enum GameStatus {
  Waiting = "waiting",
  Searching = "searching",
  Playing = "playing",
  Finished = "finished",
}

export type GameDetails = {
  id: string;
  result: GameResult;
  duration: number;
  players: (GamePlayerCreate & { player: PlayerSummary | null })[];
};
