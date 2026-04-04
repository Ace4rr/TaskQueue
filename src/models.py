from datetime import datetime
from .descriptors import (
    ShortSummaryDescriptor,
    TaskCreatedAtField,
    TaskDescriptionField,
    TaskIdField,
    TaskPriorityField,
    TaskStatusField,
)


class Task:
    """Base task model 2"""

    id=TaskIdField()
    description=TaskDescriptionField()
    priority = TaskPriorityField()
    status = TaskStatusField()
    created_at = TaskCreatedAtField()
    short_summary=ShortSummaryDescriptor()
    __slots__=("_id","_description","_priority","_status","_created_at")

    def __init__(
            self,id:str,description:str,priority:int,status:int,created_at:datetime)->None:
        self.id=id 
        self.description=description
        self.priority=priority
        self.status=status
        self.created_at=created_at

    @property
    def is_ready(self)->bool:
        """Property"""
        return self.status in {"ready", "todo", "pending"} and (self.priority>0)
    
    def __repr__(self)->str:
        return(f"Task(id={self.id!r}, description={self.description!r}, "f"priority={self.priority!r}, status={self.status!r}, "f"created_at={self.created_at!r})")