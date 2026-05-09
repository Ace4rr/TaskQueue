from typing import Iterator 
from .models import Task

class TaskQueue:
    def __init__(self)->None:
        self._tasks: list[Task]=[]
    def add(self,task: Task)->None:
        self._tasks.append(task)
    def __iter__(self)->Iterator[Task]:
        return iter(self._tasks)
    
    def __len__(self)->int:
        return len(self._tasks)

    def filter_by_status(self,status:str)->Iterator[Task]:
        return (task for task in self._tasks if task.status==status)
    
    def filter_by_priority(self,min_priority: int)-> Iterator[Task]:
        return (task for task in self._tasks if task.priority >= min_priority)
    
    def filter_by_status_and_priority(
        self, status: str, min_priority: int) -> Iterator[Task]:
        return ( task for task in self._tasks if task.status==status and task.priority>=min_priority)