from datetime import datetime
from app.schemas.task import StepState, TaskState, Task


class StateManager:
    def mark_step_running(self, step):
        step.status = StepState.RUNNING
        step.updated_at = datetime.utcnow()

    def mark_step_completed(self, step, result: str):
        step.status = StepState.COMPLETED
        step.result = result
        step.updated_at = datetime.utcnow()

    def mark_task_completed(self, task: Task):
        task.state = TaskState.COMPLETED
