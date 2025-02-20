from threading import Lock
import heapq
from app.models.job import Job, JobStatus
from typing import Optional, TypeAlias

# Type alias for priority tuple (negative_priority, submission_time)
PriorityTuple: TypeAlias = tuple[float, float]

class JobPendingQueue:
    def __init__(self) -> None:
        self._queue: list[tuple[PriorityTuple, str]] = []   # (priority_tuple, job_id)
        self._job_map: dict[str, Job] = {}                  # For O(1) job lookups
        self._lock = Lock()
        
    def enqueue(self, job: Job) -> None:
        """Thread-safe enqueue operation."""
        with self._lock:
            effective_priority = self._calculate_priority(job)
            job.status = JobStatus.PENDING
            heapq.heappush(self._queue, (effective_priority, job.id))
            self._job_map[job.id] = job
            
    def dequeue(self) -> Optional[Job]:
        """Thread-safe dequeue operation returning highest priority job."""
        with self._lock:
            while self._queue:
                _, job_id = heapq.heappop(self._queue)
                if job_id in self._job_map:
                    return self._job_map.pop(job_id)
            return None
            
            
    def peek(self) -> Optional[Job]:
        """Thread-safe peek operation."""
        with self._lock:
            while self._queue:
                _, job_id = self._queue[0]
                if job_id in self._job_map:
                    return self._job_map[job_id]
                heapq.heappop(self._queue)
            return None
        
    def remove(self, job_id: str) -> Optional[Job]:
        """Thread-safe removal of specific job."""
        with self._lock:
            if job_id in self._job_map:
                job = self._job_map.pop(job_id)
                # Note: We lazily clean up the heap when dequeuing/peeking
                return job
            return None
            
    def _calculate_priority(self, job: Job) -> PriorityTuple:
        """Calculate the priority tuple for the given job."""
        preemption_priority = float(job.preemption)
        submission_time = job.submitted_at.timestamp()
        return (preemption_priority, submission_time)