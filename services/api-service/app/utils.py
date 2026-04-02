from typing import Any

from app.models import GameResult

RATING_CHANGE = 10


def generate_updated_fields(update_data: dict[str, Any]) -> list[str]:
    fields = [f"{key} = ${i + 1}" for i, key in enumerate(update_data)]
    return fields


def calculate_rating(current_rating: int, result: GameResult, side: str) -> int:
    if result == "draw":
        return current_rating
    if result == "x_won" and side == "X" or result == "o_won" and side == "O":
        return current_rating + RATING_CHANGE
    return current_rating - RATING_CHANGE
