export type PlayerSummary = {
  userId: string;
  username: string;
  imageUrl: string;
};

export type GameResult = "x_won" | "o_won" | "draw";

export type GamePlayerCreate = {
  gameId: string;
  playerId: string | null;
  side: string;
  type: string;
};
