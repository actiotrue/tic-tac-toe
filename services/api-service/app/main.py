from contextlib import asynccontextmanager
import time
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import database
from app.api.router import api_router
from app.exceptions import EntityNotFound
from app.core.redis import redis_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    await database.connect()
    await redis_client.ping()  # type: ignore
    yield
    await database.close()
    await redis_client.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(prefix="/api/v1", router=api_router)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request_id = str(uuid.uuid7())
    logger.info(f"Request started | ID: {request_id} | {request.method} {request.url}")

    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        f"Request completed | ID: {request_id} "
        f"Status: {response.status_code} | Time {process_time:.2f}ms"
    )
    return response


@app.exception_handler(EntityNotFound)
async def entity_not_found_exception_handler(request: Request, exc: EntityNotFound):
    logger.error(f"{exc.entity_name} with id {exc.entity_id} not found")
    return JSONResponse(
        status_code=404,
        content={"message": f"{exc.entity_name} with id {exc.entity_id} not found"},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "errors": exc.errors()},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
