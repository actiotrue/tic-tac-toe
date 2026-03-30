import type { GameResult } from "@/types/shared";

export function getWinnerText(gameResult: GameResult): string {
  switch (gameResult) {
    case "x_won":
      return "X Won!";
    case "o_won":
      return "O Won";
    case "draw":
      return "Draw";
    default:
      return "Impossible";
  }
}
