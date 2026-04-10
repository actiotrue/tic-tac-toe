import uuid

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.api.deps import CurrentUserDep, GameServiceDep, InternalServiceKeyDep
from app.exceptions import InvalidGamePlayersError
from app.schemas.game import GameCreate, GameRead


router = APIRouter(prefix="/games", tags=["Game"])


@router.get("/", response_model=list[GameRead])
async def get_all_games(
    game_service: GameServiceDep,
):
    return await game_service.get_all_games()


@router.get("/{game_id}", response_model=GameRead)
async def get_game_by_id(
    game_service: GameServiceDep,
    game_id: uuid.UUID,
):
    game = await game_service.get_game_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )
    return game


@router.post("/service", response_model=GameRead, status_code=status.HTTP_201_CREATED)
async def create_game_internal(
    _: InternalServiceKeyDep,
    game_service: GameServiceDep,
    game_in: GameCreate,
):
    try:
        game = await game_service.create_game(game_in)
        return game
    except InvalidGamePlayersError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough players to create a game",
        )


@router.post("/", response_model=GameRead, status_code=status.HTTP_201_CREATED)
async def create_game(
    current_user: CurrentUserDep,
    game_service: GameServiceDep,
    game_in: GameCreate,
):
    try:
        game = await game_service.create_game(game_in)
        return game
    except InvalidGamePlayersError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough players to create a game",
        )
