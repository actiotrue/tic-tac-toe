import { onUnmounted, ref } from "vue";

import type { GameBoard, PlayerSymbol } from "@/types/game";
import type { PlayerInfo } from "@/types/player";
import type { GameClosedMessage, GameOverMessage, GameStateMessage, PlayerSearchingMessage, RematchStateMessage, WebsocketMessage } from "@/types/ws";

import { getWsTicket } from "@/api/auth";
import { GameStatus } from "@/types/game";
import { GameEvent } from "@/types/ws";

import { useWebSocket } from "../lib/ws/useWebsocket";
import { useGameState } from "./useGameState";
import { useTurnTimer } from "./useTurnTimer";

type MessageHandlerMap = {
  [GameEvent.SearchingOpponent]: (msg: PlayerSearchingMessage) => void;
  [GameEvent.GameState]: (msg: GameStateMessage) => void;
  [GameEvent.GameOver]: (msg: GameOverMessage) => void;
  [GameEvent.RematchState]: (msg: RematchStateMessage) => void;
  [GameEvent.GameClosed]: (msg: GameClosedMessage) => void;
};

export function useOnlineGame() {
  const game = useGameState();
  const timer = useTurnTimer(30);

  const wsUrl = ref("");
  const me = ref<PlayerInfo | null>(null);
  const opponent = ref<PlayerInfo | null>(null);
  const playerSide = ref<PlayerSymbol | null>(null);

  const gameStatus = ref<GameStatus>(GameStatus.Waiting);
  const error = ref<string | null>(null);

  const rematchReady = ref<Map<string, boolean>>(new Map());
  const isGameClosed = ref<boolean>(false);

  const initWebSocket = async () => {
    try {
      const ticket = await getWsTicket();
      wsUrl.value = `${import.meta.env.VITE_WS_URL}/game?ticket=${ticket}`;
    }
    catch (err) {
      console.error("Failed to get WS ticket", err);
    }
  };

  const ws = useWebSocket<WebsocketMessage>(wsUrl);

  const searchGame = () => {
    return ws.send({ type: "joinQueue" });
  };

  const makeMove = (index: number) => {
    return ws.send({ type: "makeMove", payload: { index } });
  };

  const leaveWaitingQueue = () => {
    return ws.send({ type: "leaveQueue" });
  };

  const sendRematchRequest = () => {
    return ws.send({ type: "rematchRequest" });
  };

  const startNewGame = () => {
    return ws.send({ type: "newGame" });
  };

  const handleSearching = () => {
    gameStatus.value = GameStatus.Searching;
  };

  const handleGameState = (msg: GameStateMessage) => {
    if (gameStatus.value === GameStatus.Finished) {
      return;
    }
    timer.start(msg.payload.secondsLeft);
    gameStatus.value = GameStatus.Playing;
    game.setState({ board: msg.payload.board.map(c => (c === "" ? null : c)) as GameBoard, currentPlayerSymbol: msg.payload.turn });
    playerSide.value = msg.payload.yourSide;
    me.value = msg.payload.players.find(p => p.side === msg.payload.yourSide)!;
    opponent.value = msg.payload.players.find(p => p.side !== msg.payload.yourSide)!;
  };

  const handleGameOver = (msg: GameOverMessage) => {
    gameStatus.value = GameStatus.Finished;
    rematchReady.value.clear();
    timer.stop();
    game.setState({ winner: msg.payload.winner, winningLine: msg.payload.winningLine });
  };

  const handleRematchState = (msg: RematchStateMessage) => {
    rematchReady.value.clear();
    Object.entries(msg.payload.ready).forEach(([key, value]) => {
      rematchReady.value.set(key, value);
    });

    const allReady = Array.from(rematchReady.value.values()).every(v => v === true);
    if (allReady) {
      game.reset();
      timer.reset();
      gameStatus.value = GameStatus.Playing;
    }
  };

  const handleGameClosed = () => {
    gameStatus.value = GameStatus.Finished;
    isGameClosed.value = true;
  };

  const messageHandlers: MessageHandlerMap = {
    [GameEvent.SearchingOpponent]: handleSearching,
    [GameEvent.GameState]: handleGameState,
    [GameEvent.GameOver]: handleGameOver,
    [GameEvent.RematchState]: handleRematchState,
    [GameEvent.GameClosed]: handleGameClosed,
  };

  const handleGame = async () => {
    await initWebSocket();
    if (!wsUrl.value)
      return;
    ws.connect({
      onOpen: () => {
        if (gameStatus.value !== GameStatus.Waiting) {
          return;
        }
        gameStatus.value = GameStatus.Searching;
        searchGame();
      },
      onMessage: (msg) => {
        const handler = messageHandlers[msg.type as keyof MessageHandlerMap];
        handler?.(msg as any);
      },
      onError: (err) => {
        error.value = err;
      },
      onClose: (reason) => {
        error.value = reason || "Disconnected";
      },
    });
  };

  const clear = () => {
    game.reset();
    timer.reset();
    rematchReady.value.clear();
    gameStatus.value = GameStatus.Waiting;
    me.value = null;
    opponent.value = null;
    playerSide.value = null;
    error.value = null;
    isGameClosed.value = false;
  };

  onUnmounted(() => {
    timer.stop();
    ws.close();
  });

  return {
    game,
    timer,
    me,
    opponent,
    playerSide,
    gameStatus,
    error,
    rematchReady,
    isGameClosed,
    clear,
    handleGame,
    searchGame,
    makeMove,
    leaveWaitingQueue,
    sendRematchRequest,
    startNewGame,
  };
}
