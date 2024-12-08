import heapq

class Job:
    def __init__(self, name, deadline, priority):
        self.name = name
        self.deadline = deadline
        self.priority = priority

    def __lt__(self, other):
        # Compare by deadline first, then priority if deadlines are equal
        if self.deadline == other.deadline:
            return self.priority < other.priority
        return self.deadline < other.deadline

class JobScheduler:
    def __init__(self):
        self._queue = []
    
    def schedule_job(self, job):
        # Add job to heap. Here, we use job object directly assuming it's comparable
        heapq.heappush(self._queue, job)
    
    def next_job(self):
        if self._queue:
            return heapq.heappop(self._queue)
        return None

    def has_jobs(self):
        return bool(self._queue)

# Usage
scheduler = JobScheduler()
scheduler.schedule_job(Job("Project X", deadline="2024-12-10", priority=1))
scheduler.schedule_job(Job("Project Y", deadline="2024-12-08", priority=3))
scheduler.schedule_job(Job("Project Z", deadline="2024-12-08", priority=1))

while scheduler.has_jobs():
    job = scheduler.next_job()
    print(f"Processing {job.name} with deadline {job.deadline} and priority {job.priority}")

# This would output:
# Processing Project Z with deadline 2024-12-08 and priority 1
# Processing Project Y with deadline 2024-12-08 and priority 3
# Processing Project X with deadline 2024-12-10 and priority 1



#================== Using @dataclass ==================
from dataclasses import dataclass
import heapq

@dataclass(order=True)
class Job:
    # Use `order=True` to automatically generate comparison methods based on field order
    deadline: str
    priority: int
    name: str

    # Since 'order=True', dataclass will use these fields for comparison in order:
    # 1. deadline, 2. priority, 3. name (if needed)
    # We don't need to define __lt__ manually here, but if you want to customize:
    # def __lt__(self, other):
    #     if self.deadline == other.deadline:
    #         return self.priority < other.priority
    #     return self.deadline < other.deadline

class JobScheduler:
    def __init__(self):
        self._queue = []
    
    def schedule_job(self, job):
        heapq.heappush(self._queue, job)
    
    def next_job(self):
        if self._queue:
            return heapq.heappop(self._queue)
        return None

    def has_jobs(self):
        return bool(self._queue)

# Usage
scheduler = JobScheduler()
scheduler.schedule_job(Job(deadline="2024-12-10", priority=1, name="Project X"))
scheduler.schedule_job(Job(deadline="2024-12-08", priority=3, name="Project Y"))
scheduler.schedule_job(Job(deadline="2024-12-08", priority=1, name="Project Z"))

while scheduler.has_jobs():
    job = scheduler.next_job()
    print(f"Processing {job.name} with deadline {job.deadline} and priority {job.priority}")

# This would output:
# Processing Project Z with deadline 2024-12-08 and priority 1
# Processing Project Y with deadline 2024-12-08 and priority 3
# Processing Project X with deadline 2024-12-10 and priority 1