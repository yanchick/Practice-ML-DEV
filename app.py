import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from src.api.routes import api_router
from src.infrastructure.database.utils import init_db

app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def get_webui():
    return FileResponse("index.html")


def start_service(port="8002", host="127.0.0.1", resetdb=True):
    host = os.getenv("HOST", host)
    port = int(os.getenv("PORT", port))
    if resetdb:
        init_db(drop_all=True)
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    start_service
