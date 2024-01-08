"""FastAPI router module."""
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from . import crud, schemas, database

app = FastAPI()
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"])


database.Base.metadata.create_all(bind=database.engine)


def get_db():
    """Connect to DB."""
    db = database.SessionLocal()
    try:
        crud.sync_models(db)
        yield db
    finally:
        db.close()


@app.get("/models")
async def list_models(db: Session = Depends(get_db)) -> list[schemas.LearnModel]:
    """List available ML models"""

    return crud.list_models(db)


@app.get("/balance/{id}")
async def get_balance(user_id: int, db: Session = Depends(get_db)) -> schemas.Balance:
    """Get my balance."""

    return schemas.Balance(balance=crud.get_balance(user_id, db))


@app.get("/jobs")
async def list_jobs(user_id: int, db: Session = Depends(get_db)) -> list[schemas.Job]:
    """List my jobs."""

    return crud.list_jobs(user_id, db)


@app.get("/jobs/{job_id}")
async def get_job(
    user_id: int, job_id: int, db: Session = Depends(get_db)
) -> schemas.Job:
    """List my jobs."""

    return crud.get_job(user_id, job_id, db)


@app.post("/jobs")
async def start_job(
    user_id: int, job: schemas.JobCreate, db: Session = Depends(get_db)
) -> schemas.Job:
    """Create a new job."""

    return crud.start_job(user_id, job.model_id, db)
