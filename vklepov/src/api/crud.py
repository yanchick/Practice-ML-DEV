"""Data access wrappers."""
from datetime import datetime
import json
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from src.prediction import prediction_models

from . import models, schemas


async def list_models():
    return prediction_models.values()


async def get_model(id: str):
    if id not in prediction_models:
        return None
    return prediction_models[id]


async def get_balance(uid: int, db: AsyncSession):
    debit = await db.execute(
        select(func.sum(models.BalanceDebit.amount)).where(
            models.BalanceDebit.user_id == uid
        )
    )
    debit_sum = debit.scalar()

    hold = await db.execute(
        select(func.sum(models.Job.cost)).where(
            models.Job.status != schemas.JobStatus.failed, models.Job.user_id == uid
        )
    )
    credit_sum = hold.scalar()

    return (debit_sum if debit_sum else 0) - (credit_sum if credit_sum else 0)


async def deposit_balance(uid: int, amount: int, db: AsyncSession):
    await db.execute(insert(models.BalanceDebit).values(user_id=uid, amount=amount))
    await db.commit()


async def list_jobs(uid: int, db: AsyncSession):
    """List all jobs."""

    res = await db.execute(
        select(models.Job.id, models.Job.status, models.Job.cost, models.Job.created_at)
        .where(models.Job.user_id == uid)
        .order_by(models.Job.created_at.desc())
    )

    return res.all()


async def get_job(uid: int, job_id: int, db: AsyncSession):
    """Get job by id."""
    res = await db.execute(
        select(models.Job).where(models.Job.id == job_id, models.Job.user_id == uid)
    )

    record = res.first()[0]
    res = schemas.Job(**record.__dict__)
    if record.result:
        res.result = json.loads(record.result)
    return res


async def start_job(user_id: int, model_cost: int, db: AsyncSession):
    """Start job."""

    stmt = (
        insert(models.Job)
        .values(
            user_id=user_id,
            status=schemas.JobStatus.pending,
            cost=model_cost,
            created_at=datetime.now(),
        )
        .returning(models.Job.id)
    )
    res = await db.execute(stmt)
    await db.commit()
    return res.scalar()


async def finish_job(job_id: int, status: schemas.JobStatus, payload, db: AsyncSession):
    res_text = json.dumps(payload)
    stmt = (
        update(models.Job)
        .where(models.Job.id == job_id)
        .values(status=status, result=res_text)
    )
    await db.execute(stmt)
    await db.commit()
