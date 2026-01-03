from typing import Dict
from core.job import Job


class JobStore:
    def __init__(self):
        self._jobs: Dict[str, Job] = {}

    def add(self, job: Job) -> None:
        self._jobs[job.id] = job

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def all(self):
        return list(self._jobs.values())


job_store = JobStore()
