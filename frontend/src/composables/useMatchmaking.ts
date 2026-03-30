import { ref } from "vue";

import type { Cell, GameBoard, PlayerSymbol, Winner } from "@/types/game";

import { GameStatus } from "@/types/game";

import { useWebSocket } from "./useWebsocket";

enum GameEvent {
  SearchingOpponent = "searchingOpponent",
  GameStarted = "gameStarted",
  GameState = "gameState",
  GameOver = "gameOver",
}

type PlayerSearchingMessage = { type: GameEvent.SearchingOpponent; payload: null };
type GameStartedMessage = {
  type: GameEvent.GameStarted;
  payload: { gameId: string; yourSide: PlayerSymbol; opponentId: string; turn: PlayerSymbol };
};
type GameStateMessage = {
  type: GameEvent.GameState;
  payload: { board: string[]; turn: PlayerSymbol };
};
type GameOverMessage = {
  type: GameEvent.GameOver;
  payload: { winner: Winner; winningLine: number[] | null };
};

type WebsocketMessage
  = | PlayerSearchingMessage
    | GameStartedMessage
    | GameStateMessage
    | GameOverMessage;

function isPlayerSearchingMessage(msg: WebsocketMessage): msg is PlayerSearchingMessage {
  return msg.type === GameEvent.SearchingOpponent;
}

function isGameStartedMessage(msg: WebsocketMessage): msg is GameStartedMessage {
  return msg.type === GameEvent.GameStarted;
}

function isGameStateMessage(msg: WebsocketMessage): msg is GameStateMessage {
  return msg.type === GameEvent.GameState;
}

function isGameOverMessage(msg: WebsocketMessage): msg is GameOverMessage {
  return msg.type === GameEvent.GameOver;
}

export function useMatchmaking() {
  const board = ref<GameBoard>(Array.from<Cell>({ length: 9 }).fill(null));
  const playerSide = ref<PlayerSymbol>();
  const currentPlayer = ref<PlayerSymbol>("X");
  const winner = ref<Winner | null>(null);
  const winningLine = ref<number[] | null>(null);

  const gameStatus = ref<GameStatus>(GameStatus.Waiting);
  const error = ref<string | null>(null);

  const token = localStorage.getItem("accessToken");
  const ws = useWebSocket<WebsocketMessage>(`ws://localhost:8080/api/v1/ws/game?token=${token}`);

  const searchGame = () => {
    return ws.send({ type: "joinQueue" });
  };

  const makeMove = (index: number) => {
    return ws.send({ type: "makeMove", payload: { index } });
  };

  const leaveGame = () => {
    return ws.send({ type: "leaveQueue" });
  };

  const handleGame = () => {
    ws.connect({
      onOpen: () => searchGame(),
      onMessage: (msg) => {
        switch (msg.type) {
          case GameEvent.SearchingOpponent:
            if (!isPlayerSearchingMessage(msg))
              return;
            gameStatus.value = GameStatus.Searching;
            break;
          case GameEvent.GameStarted:
            if (!isGameStartedMessage(msg))
              return;
            gameStatus.value = GameStatus.Playing;
            playerSide.value = msg.payload.yourSide;
            currentPlayer.value = msg.payload.turn;
            break;
          case GameEvent.GameState:
            if (!isGameStateMessage(msg))
              return;
            board.value = msg.payload.board.map(c => (c === "" ? null : c)) as GameBoard;
            currentPlayer.value = msg.payload.turn;
            break;
          case GameEvent.GameOver:
            if (!isGameOverMessage(msg))
              return;
            gameStatus.value = GameStatus.Finished;
            winner.value = msg.payload.winner;
            winningLine.value = msg.payload.winningLine;
            break;
        }
      },
      onError: (err) => {
        error.value = err;
      },
      onClose: (reason) => {
        error.value = reason;
      },
    });
  };

  return {
    board,
    playerSide,
    currentPlayer,
    winner,
    winningLine,
    gameStatus,
    error,
    handleGame,
    searchGame,
    makeMove,
    leaveGame,
  };
}
