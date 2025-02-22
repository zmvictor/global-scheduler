from app.core.queue import JobPendingQueue
from app.core.resource_manager import GlobalResourceManager
from app.models.job import Job
from typing import Optional
import time
import threading


SCHED_INTERVAL_SEC = 5
SCHED_BATCH_SIZE = 5


class Scheduelr:
    def __init__(
        self, 
        job_queue: JobPendingQueue, 
        grm: GlobalResourceManager,
        sched_interval_sec: int = SCHED_INTERVAL_SEC,
        sched_batch_size: int = SCHED_BATCH_SIZE
    ) -> None:
        self._job_queue = job_queue
        self._grm = grm
        self._sched_interval_sec = sched_interval_sec
        self._sched_batch_size = sched_batch_size
        
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        
    def start(self) -> None:
        # keep pulling form job queue and place the job if possible
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()
        
    def stop(self) -> None:
        self._stop_event.set()
        self._worker_thread.join()
        
    def _worker(self) -> None:
        while not self._stop_event.is_set():
            for _ in range(self._sched_batch_size):
                job = self._job_queue.dequeue()
                if not job:
                    break
                self._place_job(job)
                
            time.sleep(self._sched_interval_sec)
            
    def _place_job(self, job: Job) -> bool:
        allocatable, clusters = self._grm.allocate(job)
        if allocatable:
            return True