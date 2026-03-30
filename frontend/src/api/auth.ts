import type { AuthResponse, UserResponse } from "@/types/api";

import api from "@/api/axiosConfig";

export async function signup(username: string, password: string): Promise<string> {
  const response = await api.post<string>("/signup", { username, password });
  return response.data;
}

export async function login(username: string, password: string): Promise<AuthResponse> {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);
  const response = await api.post<AuthResponse>("/login/access-token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return response.data;
}

export async function getMe(): Promise<UserResponse> {
  const response = await api.get<UserResponse>("/me");
  return response.data;
}

export async function logout(): Promise<void> {
  await api.post("/logout");
}
