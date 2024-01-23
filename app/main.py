from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import user, model
from database import Base, engine
from scripts import insert_models
import os

from celery import Celery
from celery_config import broker_url

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware for handling browser restrictions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(user.router)
app.include_router(model.router)

# Create tables in the database
def init_db():
    Base.metadata.create_all(bind=engine)

# Startup event to initialize the database
@app.on_event("startup")
async def startup_event():
    init_db()
    print("OK\n")
    insert_models()

celery = Celery(
    'tasks',
    broker=broker_url,
    include=['tasks.inference'],  # Add your task module here
)

celery.conf.update(
    result_backend=os.getenv('BROKER_URL'),
    # Add other Celery configuration parameters here
)
# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
