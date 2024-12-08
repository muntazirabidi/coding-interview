from dataclasses import dataclass
from typing import Any
from minheap import MinHeap

# First, let's create our Task class using @dataclass
@dataclass
class Task:
    name: str                # Task name
    priority: int            # Priority (lower number = higher priority)
    
    # We still need to define how tasks should be compared
    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            raise TypeError("Can only compare Task with another Task")
        return self.priority < other.priority

# Now let's use this with our MinHeap
class TaskHeap(MinHeap):    # Inherits from our original MinHeap
    def add_task(self, name: str, priority: int) -> None:
        """Add a new task to the heap"""
        new_task = Task(name, priority)
        self.insert(new_task)
    
    def get_next_task(self) -> Task:
        """Get the highest priority task"""
        return self.remove_min()
      
      
      
def demonstrate_task_system():
    # Create our task management system
    task_manager = TaskHeap()
    
    # Add some tasks
    print("Adding tasks to the system...")
    task_manager.add_task("Fix critical production bug", 1)
    task_manager.add_task("Prepare team presentation", 3)
    task_manager.add_task("Code review", 2)
    task_manager.add_task("Emergency server maintenance", 1)
    
    # Process all tasks in priority order
    print("\nProcessing tasks by priority:")
    while not task_manager.is_empty():
        next_task = task_manager.get_next_task()
        print(f"Now handling: {next_task.name} (Priority: {next_task.priority})")


if __name__ == "__main__":
  demonstrate_task_system()