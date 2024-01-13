from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks, HTTPException
from .database import get_async_session
from . import schemas, crud, users
from src.prediction import predict

router = APIRouter()


@router.get("/models")
async def list_models() -> list[schemas.LearnModel]:
    """List available ML models"""

    return await crud.list_models()


@router.get("/balance")
async def get_balance(
    user=Depends(users.current_user), db=Depends(get_async_session)
) -> schemas.Balance:
    """Get my balance."""

    return schemas.Balance(balance=await crud.get_balance(user.id, db))


@router.post("/balance/deposit")
async def deposit_balance(
    balance: schemas.Deposit,
    user=Depends(users.current_user),
    db=Depends(get_async_session),
) -> schemas.Balance:
    """Get my balance."""

    await crud.deposit_balance(user.id, balance.amount, db)
    return schemas.Balance(balance=await crud.get_balance(user.id, db))


@router.get("/jobs")
async def list_jobs(
    user=Depends(users.current_user), db=Depends(get_async_session)
) -> list[schemas.JobShort]:
    """List my jobs."""

    return await crud.list_jobs(user.id, db)


@router.get("/jobs/{job_id}")
async def get_job(
    job_id: int, user=Depends(users.current_user), db=Depends(get_async_session)
) -> schemas.Job:
    """List my jobs."""

    return await crud.get_job(user.id, job_id, db)


@router.post("/jobs")
async def start_job(
    model_id: str,
    file: UploadFile,
    bg: BackgroundTasks,
    user=Depends(users.current_user),
    db=Depends(get_async_session),
) -> schemas.Job:
    """Create a new job."""

    model = await crud.get_model(model_id)
    if not model:
        raise HTTPException(404, f"model {model_id} not found")
    balance = await crud.get_balance(user.id, db)
    if balance < model.cost:
        raise HTTPException(400, "Insufficeient balance to run model")
    job_id = await crud.start_job(user.id, model.cost, db)

    async def on_finish(is_success: bool, payload):
        status = schemas.JobStatus.completed if is_success else schemas.JobStatus.failed
        await crud.finish_job(job_id, status, payload, db)

    bg.add_task(predict, "random-forest", file.file, on_finish)
    return await crud.get_job(user.id, job_id, db)
