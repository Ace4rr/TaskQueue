#Data и non-data дескрипторы
from datetime import datetime
from typing import Any 
from .exceptions import(    EmptyTaskIdError,
    InvalidCreatedAtError,
    InvalidDescriptionError,
    InvalidPriorityError,
    InvalidStatusError,
)

class BaseField:
    """File descriptor with valudation"""
    
    def __set_name__(self,owner:type,name:str)->None:
        self.public_name=name 
        self.storage_name=f"_{name}"

    def __get__(self,obj:Any,objtype:type|None=None)->Any:
        if obj is None:
            return self
        return getattr(obj,self.storage_name)
    
    def __set__(self,obj:Any,value:Any)->None:
        self.validate(value)
        object.__setattr__(obj,self.storage_name,self.normalize(value))

    def validate(self,value:Any)->None:
        raise NotImplementedError
    
    def normalize(self,value:Any)->Any:
        return value 
    
class TaskIdField(BaseField):
    def validate(self,value:Any)->None:
        if not isinstance(value,str):
            raise EmptyTaskIdError("Task must be a str")
        if not value.strip():
            raise EmptyTaskIdError("Task must be not empty")
    def normalize(self,value:str)->str:
        return value.strip()
    
class TaskDescriptionField(BaseField):
    def validate(self, value:Any)->None:
        if not isinstance(value,str):
            raise InvalidDescriptionError("Task description must be a str")
        
    def normalize(self,value:str)->str:
        return value.strip()
    
class TaskPriorityField(BaseField):
    def validate(self, value:Any)->None:
        if not isinstance(value,int) or isinstance(value,bool):
            raise InvalidPriorityError("Task priority must be an int")
        if value<0:
            raise InvalidPriorityError("Task priority must be >=0")
        
class TaskStatusField(BaseField):
    Allowed={"ready", "pending", "todo", "done", "blocked"}

    def validate(self, value:Any)->None:
        if not isinstance(value,str): 
            raise InvalidStatusError("Task must be a str")
        
        normalized=value.strip().lower()
        if normalized not in self.Allowed:
            raise InvalidStatusError(f"Invalid task status: {value!r}")
        
    def normalize(self,value:str)->str:
        return value.strip().lower()

class TaskCreatedAtField(BaseField):
    def validate(self,value:Any)->None:
        if not isinstance(value,datetime):
            raise InvalidCreatedAtError("Task creation date must be datetime")
        
class ShortSummaryDescriptor:
    """Non data descriptor """
    def __get__(self,obj:Any,objtype:type|None=None)->str:
        if obj is None:
            return self 
        text=obj.description
        if len(text)<=30:
            return text 
        else:
            return text[:27]+"..."