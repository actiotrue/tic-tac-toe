import type { GameDetailsResponse, PlayerResponse, PlayerUpdate, RankedPlayerResponse } from "@/types/api";

import api from "@/api/axiosConfig";

export async function getMeWithRank(): Promise<RankedPlayerResponse> {
  const response = await api.get<RankedPlayerResponse>("/players/me/rank");
  return response.data;
}

export async function getMe(): Promise<PlayerResponse> {
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

export async function getRecentGames(userId: string, limit: number, offset: number): Promise<GameDetailsResponse[]> {
  const response = await api.get<GameDetailsResponse[]>(`/players/${userId}/recent-games`, {
    params: {
      limit,
      offset,
    },
  });
  return response.data;
}

export async function getPlayerWithRank(userId: string): Promise<RankedPlayerResponse> {
  const response = await api.get<RankedPlayerResponse>(`/players/${userId}/rank`);
  return response.data;
}
