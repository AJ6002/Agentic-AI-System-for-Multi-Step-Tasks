# # import uuid
# # from fastapi import APIRouter
# # from fastapi.responses import StreamingResponse

# # from app.schemas.task import Task, RunTaskRequest
# # from app.agents.planner import plan
# # from app.orchestrator.dispatcher import Dispatcher
# # from app.streaming.streamer import stream_events
# # # from fastapi.responses import StreamingResponse
# # # from app.streaming.streamer import stream_events
# # router = APIRouter()
# # from app.streaming.streamer import stream_task


# # @router.post("/run-task")
# # def run_task(request: RunTaskRequest):
# #     task_id = str(uuid.uuid4())

# #     steps = plan(request.user_input)

# #     task = Task(
# #         task_id=task_id,
# #         user_input=request.user_input,
# #         steps=steps
# #     )

# #     dispatcher = Dispatcher()
# #     dispatcher.dispatch_plan(task_id, steps)

# #     return {
# #         "task_id": task_id,
# #         "steps_created": len(steps)
# #     }


# # @router.get("/stream")
# # def stream():
# #     return StreamingResponse(
# #         stream_events(),
# #         media_type="text/event-stream"
# #     )
# # @router.get("/stream/{task_id}")
# # def stream(task_id: str, replay: bool = False):
# #     return StreamingResponse(
# #         stream_task(task_id, replay),
# #         media_type="text/event-stream"
# #     )




# import uuid
# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse

# from app.schemas.task import Task, RunTaskRequest
# from app.agents.planner import plan
# from app.orchestrator.dispatcher import Dispatcher
# from app.streaming.streamer import stream_task

# router = APIRouter()


# @router.post("/run-task")
# def run_task(request: RunTaskRequest):
#     task_id = str(uuid.uuid4())

#     steps = plan(request.user_input)

#     task = Task(
#         task_id=task_id,
#         user_input=request.user_input,
#         steps=steps
#     )

#     dispatcher = Dispatcher()
#     dispatcher.dispatch_plan(task_id, steps)

#     return {
#         "task_id": task_id,
#         "steps_created": len(steps)
#     }


# @router.get("/stream/{task_id}")
# def stream_task_endpoint(task_id: str, replay: bool = False):
#     return StreamingResponse(
#         stream_task(task_id, replay),
#         media_type="text/event-stream",
#         headers={
#             "Cache-Control": "no-cache",
#             "Connection": "keep-alive",
#         },
#     )


# from fastapi import APIRouter
# from app.utils.metrics import TASK_METRICS_STORE

# router = APIRouter()

# @router.get("/metrics/{task_id}")
# def get_metrics(task_id: str):
#     return TASK_METRICS_STORE.get(task_id, {"error": "Metrics not found"})


import uuid
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.task import RunTaskRequest
from app.agents.planner import plan
from app.queue.redis_queue import RedisQueue
from app.streaming.streamer import stream_task

router = APIRouter()

@router.post("/run-task")
def run_task(req: RunTaskRequest):
    task_id = str(uuid.uuid4())
    steps = plan(req.user_input)
    RedisQueue().enqueue_plan(task_id, steps)

    return {
        "task_id": task_id,
        "steps_created": len(steps)
    }

@router.get("/stream/{task_id}")
def stream(task_id: str):
    return StreamingResponse(
        stream_task(task_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )
