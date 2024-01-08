"""Data access wrappers."""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import models, schemas


def list_models(db: Session):
    return db.query(models.LearnModel).all()


def sync_models(db: Session):
    db.query(models.LearnModel).delete()
    db_option = models.LearnModel(description="Baseline model, 0.97 accuracy", cost=100)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)


def get_balance(uid: int, db: Session):
    raw_balance = (
        db.query(models.BalanceDebit).filter(models.BalanceDebit.user_id == uid).first()
    )
    hold = (
        db.query(func.sum(models.Job.cost))
        .filter(
            models.Job.status == schemas.JobStatus.pending, models.Job.user_id == uid
        )
        .scalar()
    )
    return raw_balance - hold


def list_jobs(uid: int, db: Session):
    """List all jobs."""
    return (
        db.query(models.Job)
        .filter(models.Job.user_id == uid)
        .with_entities(models.Job.id, models.Job.status)
        .order_by(models.Job.created_at.desc())
    )


def get_job(uid: int, job_id: int, db: Session):
    """Get job by id."""
    return (
        db.query(models.Job)
        .filter(models.Job.id == job_id, models.Job.user_id == uid)
        .first()
    )


def start_job(user_id: int, model_id: int, db: Session):
    """Start job."""

    model_cost = db.query(models.LearnModel).get(model_id).cost
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
