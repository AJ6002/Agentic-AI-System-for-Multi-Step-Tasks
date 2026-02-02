# from app.schemas.task import ExecutionStep


# def plan(task_text: str):
#     return [
#         ExecutionStep(step_id=1, agent="retriever", payload="Research topic"),
#         ExecutionStep(step_id=2, agent="analyzer", payload="Analyze findings"),
#         ExecutionStep(step_id=3, agent="writer", payload="Write summary"),
#     ]

from app.schemas.task import ExecutionStep
from app.utils.logger import log

def plan(user_input: str):
    log("PLANNER received user task")
    log(f"PLANNER input → {user_input}")

    steps = [
        ExecutionStep(step_id=1, agent="retriever", payload="Research topic"),
        ExecutionStep(step_id=2, agent="analyzer", payload="Analyze research"),
        ExecutionStep(step_id=3, agent="writer", payload="Write final report"),
    ]

    for step in steps:
        log(
            f"PLANNER created step {step.step_id} → {step.agent.upper()}",
            agent="planner"
        )

    return steps
