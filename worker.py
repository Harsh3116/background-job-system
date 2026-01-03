import time
from datetime import datetime
from core import job
from core.job_repository import get_job, save_job

from core.redis_client import redis_client
from core.job_store import job_store
from core.job import JobStatus


def run_worker():
    print("Worker started (Redis mode)...")

    while True:
        # BLPOP blocks until an item is available
        result = redis_client.blpop("job_queue", timeout=5)

        if not result:
            continue

        _, job_id = result
        job = get_job(job_id)


        if not job:
            print(f"Job {job_id} not found in store")
            continue

        try:
            print(f"Processing job {job.id}")

            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()
            save_job(job)


            # Simulate failure
            if job.type == "fail":
                raise Exception("Simulated job failure")

            time.sleep(5)

            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            save_job(job)

            job.error_message = None

            print(f"Completed job {job.id}")

        except Exception as e:
                job.retry_count += 1
                job.error_message = str(e)

                if job.retry_count >= job.max_retries:
                    job.status = JobStatus.FAILED
                    save_job(job)
                else:
                    job.status = JobStatus.PENDING
                    save_job(job)
                    redis_client.lpush("job_queue", job.id)

                print(f"Job {job.id} failed, retry {job.retry_count}")
if __name__ == "__main__":
    run_worker()
