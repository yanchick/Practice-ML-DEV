import os
import uvicorn

from fastapi import FastAPI
from src.api.v1.routes import api_router


app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "7999"))
    uvicorn.run(app, host=host, port=port)
