from app.queue.redis_queue import RedisQueue


class Dispatcher:
    def __init__(self):
        self.queue = RedisQueue()

    def dispatch_plan(self, task_id: str, steps):
        self.queue.enqueue_plan(task_id, steps)
