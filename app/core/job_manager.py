from app.core.queue import JobPendingQueue
from app.models.job import Job
from datetime import datetime

class JobManager:
    def __init__(self) -> None:
        self._queue = JobPendingQueue()
        
    def get_job_queue(self) -> JobPendingQueue:
        return self._queue
    
    def submit_job(self, job: Job) -> bool:
        job.submitted_at = datetime.now()
        self._queue.enqueue(job)
        
    def cancel_job(self, job_id: str) -> bool:
        job = self._queue.get(job_id)
        if job:
            self._queue.remove(job_id)
            return True
        return False