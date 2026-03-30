import type { GamePlayerCreate, GameResult, PlayerSummary } from "./shared";

export type AuthResponse = {
  userId: string;
  accessToken: string;
  tokenType: string;
};

export type GameCreate = {
  id: string;
  result: GameResult;
  players: GamePlayerCreate[];
  duration: number;
};

export type RecentGamesResponse = {
  id: string;
  result: GameResult;
  players: PlayerSummary[];
  duration: number;
};

export type PlayerResponse = {
  userId: string;
  username: string;
  imageUrl: string;
  rating: number;
  wins: number;
  losses: number;
  draws: number;
  createdAt: string;
  updatedAt: string;
};

export type RankedPlayerResponse = {
  rank: number;
} & PlayerResponse;

export type PlayerUpdate = {
  userId: string;
  username: string;
  imageUrl: string;
  rating: number;
  wins: number;
  losses: number;
  draws: number;
};

export type GameResponse = {
  id: string;
  result: GameResult;
  duration: number;
};

export type GameDetailsResponse = {
  players: (GamePlayerCreate & { player: PlayerSummary | null })[];
} & GameResponse;

export type UserResponse = {
  id: string;
  username: string;
};
