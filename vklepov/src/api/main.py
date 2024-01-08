"""FastAPI router module."""
from fastapi import Depends, FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from . import crud, schemas, database, users

app = FastAPI()
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.include_router(users.user_router)


# async def get_db():
#     """Connect to DB."""
#     async with database.get_async_session() as db:
#         crud.sync_models(db)
#         yield db


@app.get("/models")
async def list_models(
    db=Depends(database.get_async_session),
) -> list[schemas.LearnModel]:
    """List available ML models"""

    return await crud.list_models(db)


@app.get("/balance/{id}")
async def get_balance(
    user_id: int, db=Depends(database.get_async_session)
) -> schemas.Balance:
    """Get my balance."""

    return schemas.Balance(balance=crud.get_balance(user_id, db))


@app.get("/jobs")
async def list_jobs(
    user_id: int, db=Depends(database.get_async_session)
) -> list[schemas.Job]:
    """List my jobs."""

    return crud.list_jobs(user_id, db)


@app.get("/jobs/{job_id}")
async def get_job(
    user_id: int, job_id: int, db=Depends(database.get_async_session)
) -> schemas.Job:
    """List my jobs."""

    return crud.get_job(user_id, job_id, db)


@app.post("/jobs")
async def start_job(
    user_id: int, job: schemas.JobCreate, db=Depends(database.get_async_session)
) -> schemas.Job:
    """Create a new job."""

    return crud.start_job(user_id, job.model_id, db)
