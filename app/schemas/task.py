# from enum import Enum
# from typing import List, Optional
# from datetime import datetime
# from pydantic import BaseModel


# class TaskState(str, Enum):
#     PENDING = "PENDING"
#     RUNNING = "RUNNING"
#     COMPLETED = "COMPLETED"
#     FAILED = "FAILED"


# class StepState(str, Enum):
#     PENDING = "PENDING"
#     RUNNING = "RUNNING"
#     COMPLETED = "COMPLETED"
#     FAILED = "FAILED"


# class ExecutionStep(BaseModel):
#     step_id: int
#     agent: str
#     payload: str
#     status: StepState = StepState.PENDING
#     retries: int = 0
#     max_retries: int = 3
#     result: Optional[str] = None
#     created_at: datetime = datetime.utcnow()
#     updated_at: Optional[datetime] = None


# class Task(BaseModel):
#     task_id: str
#     user_input: str
#     state: TaskState = TaskState.PENDING
#     steps: List[ExecutionStep]
#     created_at: datetime = datetime.utcnow()


# from pydantic import BaseModel

# class RunTaskRequest(BaseModel):
#     user_input: str

from pydantic import BaseModel
from typing import List

class RunTaskRequest(BaseModel):
    user_input: str


class ExecutionStep(BaseModel):
    step_id: int
    agent: str
    payload: str


class Task(BaseModel):
    task_id: str
    user_input: str
    steps: List[ExecutionStep]
