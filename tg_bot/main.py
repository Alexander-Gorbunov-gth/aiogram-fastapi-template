from fastapi import FastAPI

from core.application import lifespan

app = FastAPI(lifespan=lifespan)

