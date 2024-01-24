import os

import fire
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.routes import api_router
from src.infrastructure.database.utils import init_db


app = FastAPI()
app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Adjust this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start_service(port="7999", host="127.0.0.1", resetdb=False):
    host = os.getenv("HOST", host)
    port = int(os.getenv("PORT", port))
    if resetdb:
        init_db(drop_all=True)
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    fire.Fire(start_service)
