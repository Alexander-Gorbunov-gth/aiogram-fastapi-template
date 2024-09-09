from fastapi import FastAPI

from core.application import lifespan

app = FastAPI(
    lifespan=lifespan,
    # root_path='/tg-bot/',
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json',
    root_path="/bot",
    )
