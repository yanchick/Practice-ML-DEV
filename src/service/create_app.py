from fastapi import FastAPI

from service.api.routes import api_router


def create_app():

    app = FastAPI()
    app.include_router(api_router)

    return app
