from sqlalchemy import text
from core.db import SessionLocal
from core.job import Job
import json
from core.job import JobStatus


def save_job(job: Job):
    session = SessionLocal()
    try:
        session.execute(
            text("""
               INSERT INTO jobs (
                id, type, status, payload,
                retry_count, max_retries,
                error_message, created_at,
                started_at, completed_at
                )
                VALUES (
                :id, :type, :status, :payload,
                :retry_count, :max_retries,
                :error_message, :created_at,
                :started_at, :completed_at
                )
                ON CONFLICT (id)
                DO UPDATE SET
                status = EXCLUDED.status,
                payload = EXCLUDED.payload,
                retry_count = EXCLUDED.retry_count,
                error_message = EXCLUDED.error_message,
                started_at = EXCLUDED.started_at,
                completed_at = EXCLUDED.completed_at;
                """),
            {
                "id": job.id,
                "type": job.type,
                "status": job.status.value,
                "payload": json.dumps(job.payload),
                "retry_count": job.retry_count,
                "max_retries": job.max_retries,
                "error_message": job.error_message,
                "created_at": job.created_at,
                "started_at": job.started_at,
                "completed_at": job.completed_at,
            }
        )
        session.commit()
    finally:
        session.close()


def get_job(job_id: str) -> Job | None:
    session = SessionLocal()
    try:
        result = session.execute(
            text("SELECT * FROM jobs WHERE id = :id"),
            {"id": job_id}
        ).mappings().first()

        if not result:
            return None

        job = Job(
            id=str(result["id"]),
            type=result["type"],
            status=JobStatus(result["status"]),
            payload=result["payload"],
            retry_count=result["retry_count"],
            max_retries=result["max_retries"],
            error_message=result["error_message"],
        )
        job.created_at = result["created_at"]
        job.started_at = result["started_at"]
        job.completed_at = result["completed_at"]

        return job
    finally:
        session.close()
