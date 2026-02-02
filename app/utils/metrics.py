import time
from app.queue.redis_queue import RedisQueue

AGENT_COST = {
    "retriever": 1,
    "analyzer": 2,
    "writer": 3,
}

class TaskMetrics:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.start_time = time.time()
        self.cost_units = 0
        self.final_result = None
        self.end_time = None
        self.queue = RedisQueue()

    def add_cost(self, agent: str):
        self.cost_units += AGENT_COST.get(agent, 1)

    def finish(self, final_result: str):
        self.end_time = time.time()
        self.final_result = final_result
        metrics = self.summary()
        self.queue.store_metrics(self.task_id, metrics)
        return metrics

    def summary(self):
        return {
            "latency_ms": int((self.end_time - self.start_time) * 1000),
            "cost_units": self.cost_units,
            "final_result": self.final_result,
        }
