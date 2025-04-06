from pydantic import BaseModel
from typing import Optional , List, Literal

class Query(BaseModel):
    attribute: str
    operator: str
    value: str


class Task(BaseModel):
    title: str
    assigned_to: List[str]  # List of user IDs or usernames
    status: str  # Enum-like status

class TaskBoard(BaseModel):
    name: str
    createdBy: str  
    members: List[str]  
    tasks: List[Task]  # Now each task is a Task object