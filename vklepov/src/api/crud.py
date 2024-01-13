"""Data access wrappers."""
from datetime import datetime
import json
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from . import models, schemas


async def list_models(db: AsyncSession):
    res = await db.execute(select(models.LearnModel))
    return res.scalars().all()


def sync_models(db: AsyncSession):
    db.query(models.LearnModel).delete()
    db_option = models.LearnModel(description="Baseline model, 0.97 accuracy", cost=100)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)


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


async def start_job(user_id: int, model_id: int, db: AsyncSession):
    """Start job."""

    ml_model = await db.get(models.LearnModel, model_id)
    model_cost = ml_model.cost
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
