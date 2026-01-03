from fastapi import FastAPI
from core import job
from core.job import Job
from core.job_store import JobStore
from core.redis_client import redis_client
from core.job_repository import save_job, get_job
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from core.job_store import job_store


@app.get("/")
def root():
    return {"message": "Background Job System is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

from pydantic import BaseModel
from typing import Any


class CreateJobRequest(BaseModel):
    type: str
    payload: Any | None = None

@app.post("/jobs")
def create_job(request: CreateJobRequest):
    job = Job(
        type=request.type,
        payload=request.payload
    )

    save_job(job)
    redis_client.lpush("job_queue", job.id)


    return {
        "job_id": job.id,
        "status": job.status
    }

@app.get("/jobs/{job_id}")
def get_job_endpoint(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "id": job.id,
        "type": job.type,
        "status": job.status,
        "retry_count": job.retry_count,
        "error_message": job.error_message,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
    }



