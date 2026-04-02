import type { GameDetailsResponse, PlayerResponse, PlayerUpdate, RankedPlayerResponse } from "@/types/api";

import api from "@/api/axiosConfig";

export async function getPlayerWithRank(): Promise<RankedPlayerResponse> {
  const response = await api.get<RankedPlayerResponse>("/players/me/rank");
  return response.data;
}

export async function getPlayer(): Promise<PlayerResponse> {
  const response = await api.get<PlayerResponse>("/players/me");
  return response.data;
}

export async function updatePlayer(player: Partial<PlayerUpdate>): Promise<PlayerResponse> {
  const response = await api.patch<PlayerResponse>("/players/me", player);
  return response.data;
}

export async function getLeaderboard(start: number, end: number): Promise<RankedPlayerResponse[]> {
  const response = await api.get<RankedPlayerResponse[]>("/players/leaderboard", {
    params: {
      start,
      end,
    },
  });
  return response.data;
}

export async function getRecentGames(limit: number, offset: number): Promise<GameDetailsResponse[]> {
  const response = await api.get<GameDetailsResponse[]>("/players/me/recent-games", {
    params: {
      limit,
      offset,
    },
  });
  return response.data;
}
