import { onUnmounted, ref } from "vue";

import type {
  OngoingGame,
  OngoingGameCreatedPayload,
  OngoingGameFinishedPayload,
  OngoingGamesSnapshotPayload,
} from "@/types/ongoing";

import { getWsTicket } from "@/api/auth";

function parseEventPayload<T>(event: Event): T | null {
  if (!(event instanceof MessageEvent) || typeof event.data !== "string") {
    return null;
  }

  try {
    return JSON.parse(event.data) as T;
  }
  catch {
    return null;
  }
}

export function useOngoingGames() {
  const games = ref<OngoingGame[]>([]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  const source = ref<EventSource | null>(null);

  const disconnect = () => {
    if (!source.value) {
      return;
    }
    source.value.close();
    source.value = null;
  };

  const connect = async () => {
    disconnect();
    isLoading.value = true;
    error.value = null;

    try {
      const ticket = await getWsTicket();
      const streamUrl = `${import.meta.env.VITE_EVENTS_URL}/ws/ongoing-games?ticket=${ticket}`;
      const eventSource = new EventSource(streamUrl);

      eventSource.addEventListener("activeGames", (event) => {
        const payload = parseEventPayload<OngoingGamesSnapshotPayload>(event);
        if (!payload) {
          return;
        }

        games.value = payload.games;
        isLoading.value = false;
        error.value = null;
      });

      eventSource.addEventListener("gameCreated", (event) => {
        const payload = parseEventPayload<OngoingGameCreatedPayload>(event);
        if (!payload) {
          return;
        }

        const exists = games.value.some(g => g.gameId === payload.game.gameId);
        if (!exists) {
          games.value = [payload.game, ...games.value];
        }
      });

      eventSource.addEventListener("gameFinished", (event) => {
        const payload = parseEventPayload<OngoingGameFinishedPayload>(event);
        if (!payload) {
          return;
        }

        games.value = games.value.filter(g => g.gameId !== payload.gameId);
      });

      eventSource.onerror = () => {
        isLoading.value = false;
        error.value = "Failed to receive active games list";
        eventSource.close();
        source.value = null;
      };

      source.value = eventSource;
    }
    catch {
      isLoading.value = false;
      error.value = "Failed to connect to games stream";
    }
  };

  onUnmounted(() => {
    disconnect();
  });

  return {
    games,
    isLoading,
    error,
    connect,
    disconnect,
  };
}
