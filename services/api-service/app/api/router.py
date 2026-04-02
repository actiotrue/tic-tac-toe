from fastapi import APIRouter
from app.api.routes import player_routes, game_routes, user_routes

api_router = APIRouter()

api_router.include_router(user_routes.router)
api_router.include_router(player_routes.router)
# api_router.include_router(game_routes.router, prefix="/ws")
api_router.include_router(game_routes.router)
