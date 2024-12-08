from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any
from enum import Enum
from minheap import MinHeap

# Define task status enum
class TaskStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    COMPLETED = "Completed"

# Define task priority levels
class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class ProjectTask:
    """
    Represents a project task with priority and scheduling information.
    Lower priority number means higher importance (1 is highest).
    """
    # Required fields
    task_id: str
    title: str
    priority: TaskPriority
    due_date: datetime
    
    # Optional fields with defaults
    assigned_to: Optional[str] = None
    description: str = ""
    estimated_hours: float = 0.0
    status: TaskStatus = TaskStatus.NOT_STARTED
    dependencies: set[str] = None
    
    def __post_init__(self):
        """Initialize collections after dataclass initialization"""
        if self.dependencies is None:
            self.dependencies = set()
    
    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, ProjectTask):
            raise TypeError("Can only compare ProjectTask with another ProjectTask")
        
        # Compare by priority first
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        
        # If same priority, compare by due date
        return self.due_date < other.due_date

class ProjectTaskManager(MinHeap):
    """Manages project tasks using a priority queue based on MinHeap"""
    
    def schedule_task(self, 
                     task_id: str,
                     title: str,
                     priority: TaskPriority,
                     due_date: datetime,
                     assigned_to: Optional[str] = None,
                     description: str = "",
                     estimated_hours: float = 0.0,
                     dependencies: set[str] = None) -> None:
        """Schedule a new task with given properties"""
        task = ProjectTask(
            task_id=task_id,
            title=title,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to,
            description=description,
            estimated_hours=estimated_hours,
            dependencies=dependencies
        )
        self.insert(task)
    
    def get_highest_priority_task(self) -> Optional[ProjectTask]:
        """Retrieve the highest priority task"""
        return self.remove_min()
    
    def peek_next_task(self) -> Optional[ProjectTask]:
        """View the next task without removing it"""
        return self.peek()

def demonstrate_project_management():
    """Demonstrate the project task management system"""
    project_manager = ProjectTaskManager()
    
    # Add various project tasks
    print("Scheduling project tasks...")
    
    # Critical priority tasks
    project_manager.schedule_task(
        task_id="PROJ-1",
        title="Fix Authentication Bug",
        priority=TaskPriority.CRITICAL,
        due_date=datetime(2024, 12, 8, 14, 0),
        assigned_to="Alice",
        description="Users unable to login - immediate attention required",
        estimated_hours=4.0
    )
    
    # High priority tasks
    project_manager.schedule_task(
        task_id="PROJ-2",
        title="Database Optimization",
        priority=TaskPriority.HIGH,
        due_date=datetime(2024, 12, 8, 16, 0),
        assigned_to="Bob",
        description="Optimize query performance for user dashboard",
        estimated_hours=6.0,
        dependencies={"PROJ-1"}
    )
    
    # Medium priority tasks
    project_manager.schedule_task(
        task_id="PROJ-3",
        title="Update Documentation",
        priority=TaskPriority.MEDIUM,
        due_date=datetime(2024, 12, 9, 12, 0),
        assigned_to="Charlie",
        description="Update API documentation with new endpoints",
        estimated_hours=3.0
    )
    
    # Process all tasks
    print("\nProcessing tasks by priority and due date:")
    while not project_manager.is_empty():
        task = project_manager.get_highest_priority_task()
        print(f"""
Task ID: {task.task_id}
Title: {task.title}
Priority: {task.priority.name}
Due: {task.due_date.strftime('%Y-%m-%d %I:%M %p')}
Assigned to: {task.assigned_to}
Status: {task.status.value}
Estimated Hours: {task.estimated_hours}
Dependencies: {', '.join(task.dependencies) if task.dependencies else 'None'}
Description: {task.description}
----------------------------------------""")

if __name__ == "__main__":
    demonstrate_project_management()