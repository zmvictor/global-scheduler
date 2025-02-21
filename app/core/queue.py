from threading import Lock
import heapq
from app.models.job import Job, JobStatus
from typing import Optional, TypeAlias, List, Dict

# Type alias for priority tuple (negative_priority, submission_time)
PriorityTuple: TypeAlias = tuple[float, float]

class JobPendingQueue:
    def __init__(self) -> None:
        self._queue = List[(PriorityTuple, str)]    # priority, job.id
        self._job_map = Dict[str, Job]              # job.id, job
        self._lock = Lock()
    
    def enqueue(self, job: Job) -> None:
        with self._lock:
            job_priority = self._calculate_priority(job)
            heapq.heappush(self._queue, (job_priority, job.id))
            job.status = JobStatus.PENDING
            self._job_map[job.id] = job
            
    def dequeue(self) -> Optional[Job]:
        with self._lock:
            while self._queue:
                _, job_id = heapq.heappop(self._queue)
                if job_id in self._job_map:
                    job = self._job_map.pop(job_id)
                    return job
            return None
    
    def peek(self) -> Optional[Job]:
        with self._lock:
            while self._queue:
                _, job_id = self._queue[0]
                if job_id in self._job_map:
                    return self._job_map[job_id]
                self.dequeue()
            return None
    
    def remove(self, job_id: str) -> None:
        with self._lock:
            self._job_map.pop(job_id, None)
    
    def get(self, job_id: str) -> Optional[Job]:
        with self._lock:
            if job_id in self._job_map:
                return self._job_map[job_id]
            return None
    
    def list_all(self) -> List[Job]:
        jobs = []
        with self._lock:
            jobs = list(self._job_map.values())
        return jobs
    
    def _calculate_priority(self, job: Job) -> PriorityTuple:
        preemption_score = float(job.preemption)
        submission_time = job.submitted_at.timestamp()
        return PriorityTuple(preemption_score, submission_time)