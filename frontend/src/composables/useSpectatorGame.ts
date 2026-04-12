import { onUnmounted, ref } from "vue";

import type { GameBoard } from "@/types/game";
import type { PlayerInfo } from "@/types/player";
import type {
  SpectatorGameClosedMessage,
  SpectatorGameOverMessage,
  SpectatorGameStateMessage,
  SpectatorWebsocketMessage,
} from "@/types/spectator";

import { getWsTicket } from "@/api/auth";
import { useWebSocket } from "@/lib/ws/useWebsocket";
import { GameStatus } from "@/types/game";

import { useGameState } from "./useGameState";
import { useTurnTimer } from "./useTurnTimer";

export function useSpectatorGame(gameId: string) {
  const game = useGameState();
  const timer = useTurnTimer(30);

  const wsUrl = ref("");
  const players = ref<PlayerInfo[]>([]);
  const gameStatus = ref<GameStatus>(GameStatus.Waiting);
  const error = ref<string | null>(null);

  const ws = useWebSocket<SpectatorWebsocketMessage>(wsUrl);

  const setStateFromMessage = (msg: SpectatorGameStateMessage) => {
    if (gameStatus.value === GameStatus.Finished) {
      return;
    }

    game.setState({
      board: msg.payload.board.map(cell => (cell === "" ? null : cell)) as GameBoard,
      currentPlayerSymbol: msg.payload.turn,
    });
    players.value = msg.payload.players;
    timer.start(msg.payload.secondsLeft);
    gameStatus.value = GameStatus.Playing;
  };

  const setGameOverFromMessage = (msg: SpectatorGameOverMessage) => {
    gameStatus.value = GameStatus.Finished;
    timer.stop();
    game.setState({
      winner: msg.payload.winner,
      winningLine: msg.payload.winningLine,
    });
  };

  const setClosedStateFromMessage = (msg: SpectatorGameClosedMessage) => {
    gameStatus.value = GameStatus.Finished;
    timer.stop();

    const reasonMap: Record<string, string> = {
      playerLeft: "Game finished: one of the players left the match",
      gameUnavailable: "Game is not available for watching",
      invalidGameId: "Invalid game identifier",
      gameClosed: "Game finished",
    };

    error.value = reasonMap[msg.payload.reason] ?? "Watching session finished";
  };

  const initWebSocket = async () => {
    const ticket = await getWsTicket();
    wsUrl.value = `${import.meta.env.VITE_WS_URL}/spectate?ticket=${ticket}&gameId=${encodeURIComponent(gameId)}`;
  };

  const connect = async () => {
    if (!gameId) {
      error.value = "Game identifier is missing";
      return;
    }

    error.value = null;
    gameStatus.value = GameStatus.Waiting;

    try {
      await initWebSocket();
    }
    catch {
      error.value = "Failed to initialize game connection";
      return;
    }

    ws.connect({
      onMessage: (msg) => {
        switch (msg.type) {
          case "gameState":
            setStateFromMessage(msg);
            break;
          case "gameOver":
            setGameOverFromMessage(msg);
            break;
          case "gameClosed":
            setClosedStateFromMessage(msg);
            break;
        }
      },
      onError: (wsError) => {
        error.value = wsError;
      },
      onClose: (reason) => {
        if (gameStatus.value !== GameStatus.Finished) {
          error.value = reason || "Connection to game stream was closed";
        }
      },
    });
  };

  const disconnect = () => {
    timer.stop();
    ws.close();
  };

  onUnmounted(() => {
    disconnect();
  });

  return {
    game,
    timer,
    players,
    gameStatus,
    error,
    connect,
    disconnect,
  };
}