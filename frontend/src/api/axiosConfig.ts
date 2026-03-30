import axios from "axios";

import type { AuthResponse } from "@/types/api";

export const API_URL = `http://${import.meta.env.VITE_API_URL}/api/v1`;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

api.interceptors.response.use(
  (config) => {
    return config;
  },
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._isRetry) {
      originalRequest._isRetry = true;
      try {
        const response = await axios.post<AuthResponse>(
          `${API_URL}/refresh`,
          {},
          { withCredentials: true },
        );
        localStorage.setItem("accessToken", response.data.accessToken);
        return api.request(originalRequest);
      }
      catch {
        localStorage.removeItem("accessToken");
      }
    }
    return Promise.reject(error);
  },
);

export default api;
