"""Data access wrappers."""
from datetime import datetime
from sqlalchemy import select, insert
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


def list_jobs(uid: int, db: AsyncSession):
    """List all jobs."""
    return (
        db.query(models.Job)
        .filter(models.Job.user_id == uid)
        .with_entities(models.Job.id, models.Job.status)
        .order_by(models.Job.created_at.desc())
    )


def get_job(uid: int, job_id: int, db: AsyncSession):
    """Get job by id."""
    return (
        db.query(models.Job)
        .filter(models.Job.id == job_id, models.Job.user_id == uid)
        .first()
    )


def start_job(user_id: int, model_id: int, db: AsyncSession):
    """Start job."""

    model_cost = db.get(models.LearnModel, model_id).cost
    db_job = models.Job(
        user_id=user_id,
        status=schemas.JobStatus.pending,
        cost=model_cost,
        created_at=datetime.now(),
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
