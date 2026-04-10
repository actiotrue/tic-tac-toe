import type { PlayerSymbol, Winner } from "./game";
import type { PlayerInfo } from "./player";

export enum GameEvent {
  SearchingOpponent = "searchingOpponent",
  GameState = "gameState",
  GameOver = "gameOver",
  RematchState = "rematchState",
  GameClosed = "gameClosed",
}

export type PlayerSearchingMessage = { type: GameEvent.SearchingOpponent; payload: null };

export type GameStateMessage = {
  type: GameEvent.GameState;
  payload: { board: string[]; turn: PlayerSymbol; yourSide: PlayerSymbol; players: PlayerInfo[]; secondsLeft: number };
};

export type GameOverMessage = {
  type: GameEvent.GameOver;
  payload: { winner: Winner; winningLine: number[] | null };
};

export type RematchStateMessage = {
  type: GameEvent.RematchState;
  payload: { ready: Record<string, boolean> };
};

export type GameClosedMessage = {
  type: GameEvent.GameClosed;
  payload: { reason: string };
};

export type WebsocketMessage
  = | PlayerSearchingMessage
    | GameStateMessage
    | GameOverMessage
    | RematchStateMessage
    | GameClosedMessage;
