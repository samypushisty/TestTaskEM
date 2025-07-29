import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.v1.base_schemas.schemas import StandartException
from core.config import settings
from core.models import db_helper
from api import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()

main_app = FastAPI(

    lifespan=lifespan,
    title="App",
)

main_app.include_router(
    api_router
)

origins = [
    "*"
    # "http://localhost:5173",
    # "http://127.0.0.1:5173",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@main_app.exception_handler(StandartException)
async def unicorn_exception_handler(request: Request, exc: StandartException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port
    )