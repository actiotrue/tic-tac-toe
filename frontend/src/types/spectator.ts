import type { PlayerSymbol, Winner } from "./game";
import type { PlayerInfo } from "./player";

export type SpectatorGameStateMessage = {
  type: "gameState";
  payload: {
    board: string[];
    turn: PlayerSymbol;
    yourSide?: PlayerSymbol | "";
    players: PlayerInfo[];
    secondsLeft: number;
  };
};

export type SpectatorGameOverMessage = {
  type: "gameOver";
  payload: {
    winner: Winner;
    winningLine: number[] | null;
  };
};

export type SpectatorGameClosedMessage = {
  type: "gameClosed";
  payload: {
    reason: string;
  };
};

export type SpectatorWebsocketMessage
  = | SpectatorGameStateMessage
    | SpectatorGameOverMessage
    | SpectatorGameClosedMessage;
