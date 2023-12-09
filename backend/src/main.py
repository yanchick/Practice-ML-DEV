from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.router import user_router, predictions_router, model_router

app = FastAPI()
app.include_router(user_router, prefix="/v1")
app.include_router(predictions_router, prefix="/v1")
app.include_router(model_router,prefix="/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

