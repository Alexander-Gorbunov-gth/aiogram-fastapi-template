from fastapi import FastAPI

from core.application import lifespan, _include_routers

app = FastAPI(lifespan=lifespan)

# @app.on_event("startup")


# _include_routers(app)
