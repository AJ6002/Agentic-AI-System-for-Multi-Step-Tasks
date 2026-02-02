from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel


class StreamEvent(BaseModel):
    event: Literal[
        "task_created",
        "planner_completed",
        "step_started",
        "step_completed",
        "task_completed",
        "task_failed",
    ]
    task_id: str
    step_id: Optional[int] = None
    data: Optional[str] = None
    timestamp: datetime = datetime.utcnow()
