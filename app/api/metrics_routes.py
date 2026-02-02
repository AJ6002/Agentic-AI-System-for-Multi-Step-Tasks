from fastapi import APIRouter
from app.queue.redis_queue import RedisQueue

router = APIRouter()

@router.get("/metrics/{task_id}")
def get_metrics(task_id: str):
    queue = RedisQueue()
    metrics = queue.get_metrics(task_id)
    return metrics if metrics else {"error": "Metrics not found"}
