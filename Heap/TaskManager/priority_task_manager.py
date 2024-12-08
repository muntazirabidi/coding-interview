from enum import Enum
from datetime import datetime
import heapq
from dataclasses import dataclass, field
from typing import Set, List

class TaskStatus(Enum):
    """Represents the current state of a task"""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    ON_HOLD = "On Hold"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class TaskPriority(Enum):
    """Defines task priority levels with corresponding numerical values for sorting"""
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    
    def __lt__(self, other):
        """Enable comparison between priority levels"""
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

@dataclass(order=True)
class ProjectTask:
    """
    Represents a project task with all its attributes and metadata.
    The sort_index is used for priority queue ordering.
    """
    sort_index: tuple = field(init=False, repr=False)
    task_id: str
    title: str
    priority: TaskPriority
    due_date: datetime
    status: TaskStatus = TaskStatus.NOT_STARTED
    assigned_to: str = ""
    description: str = ""
    estimated_hours: float = 0.0
    dependencies: Set[str] = field(default_factory=set)
    
    def __post_init__(self):
        """Set the sort index based on priority and due date for heap ordering"""
        self.sort_index = (
            -self.priority.value,  # Negative for max-heap behavior
            self.due_date
        )

class ProjectTaskManager:
    """
    Manages a collection of project tasks using a priority queue.
    Provides methods for task scheduling, retrieval, and management.
    """
    def __init__(self):
        """Initialize an empty priority queue for tasks"""
        self.heap: List[ProjectTask] = []
    
    def schedule_task(self, task_id: str, title: str, priority: TaskPriority,
                     due_date: datetime, assigned_to: str = "", description: str = "",
                     estimated_hours: float = 0.0, dependencies: Set[str] = None):
        """
        Create and schedule a new task with the given parameters
        """
        task = ProjectTask(
            task_id=task_id,
            title=title,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to,
            description=description,
            estimated_hours=estimated_hours,
            dependencies=dependencies or set()
        )
        heapq.heappush(self.heap, task)
        return task
    
    def get_highest_priority_task(self) -> ProjectTask:
        """Remove and return the highest priority task"""
        return heapq.heappop(self.heap) if self.heap else None
    
    def peek_next_task(self) -> ProjectTask:
        """View the highest priority task without removing it"""
        return self.heap[0] if self.heap else None
    
    def is_empty(self) -> bool:
        """Check if there are any tasks in the queue"""
        return len(self.heap) == 0