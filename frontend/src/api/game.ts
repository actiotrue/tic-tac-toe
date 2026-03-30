import type { GameCreate, GameResponse } from "@/types/api";

import api from "./axiosConfig";

export async function createGame(game: GameCreate): Promise<GameResponse> {
  const response = await api.post<GameResponse>("/games", game);
  return response.data;
}
