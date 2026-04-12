import type { PlayerSymbol } from "./game";
import type { PlayerInfo } from "./player";

export type OngoingGame = {
  gameId: string;
  players: PlayerInfo[];
  turn: PlayerSymbol;
  startedAt: string;
};

export type OngoingGamesSnapshotPayload = {
  games: OngoingGame[];
};

export type OngoingGameCreatedPayload = {
  game: OngoingGame;
};

export type OngoingGameFinishedPayload = {
  gameId: string;
};
