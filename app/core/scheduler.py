from app.core.queue import JobPendingQueue

class Scheduelr:
    def __init__(self, job_queue: JobPendingQueue) -> None:
        self._job_queue = job_queue
        self._resource_manager = None
        
    def start(self) -> None:
        # keep pulling form job queue and place the job if possible
        pass
        
    def stop(self) -> None:
        pass