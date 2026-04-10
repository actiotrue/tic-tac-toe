import type { PlayerSymbol } from "./game";

export type Player = {
  userId: string;
  username: string;
  rating: number;
  wins: number;
  losses: number;
  draws: number;
  imageUrl: string;
  rank: number;
  createdAt: string;
  updatedAt: string;
};

export type PlayerInfo = {
  userId: string;
  side: PlayerSymbol;
  username: string;
  imageUrl: string;
};

export type RankedPlayer = Player & {
  rank: number;
};
