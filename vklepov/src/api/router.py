from fastapi import APIRouter, Depends
from .database import get_async_session
from . import schemas, crud

router = APIRouter()


@router.get("/models")
async def list_models(db=Depends(get_async_session)) -> list[schemas.LearnModel]:
    """List available ML models"""

    return await crud.list_models(db)


@router.get("/balance/{id}")
async def get_balance(user_id: int, db=Depends(get_async_session)) -> schemas.Balance:
    """Get my balance."""

    return schemas.Balance(balance=crud.get_balance(user_id, db))


@router.get("/jobs")
async def list_jobs(user_id: int, db=Depends(get_async_session)) -> list[schemas.Job]:
    """List my jobs."""

    return crud.list_jobs(user_id, db)


@router.get("/jobs/{job_id}")
async def get_job(
    user_id: int, job_id: int, db=Depends(get_async_session)
) -> schemas.Job:
    """List my jobs."""

    return crud.get_job(user_id, job_id, db)


@router.post("/jobs")
async def start_job(
    user_id: int, job: schemas.JobCreate, db=Depends(get_async_session)
) -> schemas.Job:
    """Create a new job."""

    return crud.start_job(user_id, job.model_id, db)
