from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.router import model_router, predictions_router, user_router  # type: ignore[attr-defined]
from src.schemes.router import OpenAPIResponses
from src.settings import Settings

v1_prefix = "/v1"

app = FastAPI(responses=OpenAPIResponses.HTTP_422_UNPROCESSABLE_ENTITY)
app.include_router(user_router, prefix=v1_prefix)
app.include_router(predictions_router, prefix=v1_prefix)
app.include_router(model_router, prefix=v1_prefix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    settings = Settings()
    uvicorn.run("main:app", host=str(settings.host), port=settings.port, reload=settings.debug)
