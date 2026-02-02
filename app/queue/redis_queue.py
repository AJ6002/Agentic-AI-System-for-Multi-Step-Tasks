# # # import redis
# # # import json
# # # from collections import defaultdict
# # # from app.config import REDIS_HOST, REDIS_PORT


# # # class RedisQueue:
# # #     def __init__(self):
# # #         self.client = redis.Redis(
# # #             host=REDIS_HOST,
# # #             port=REDIS_PORT,
# # #             decode_responses=True,
# # #         )

# # #         self.stream_name = "agent_tasks"
# # #         self.group_name = "agent_workers"

# # #         # Create consumer group once
# # #         try:
# # #             self.client.xgroup_create(
# # #                 name=self.stream_name,
# # #                 groupname=self.group_name,
# # #                 id="0",
# # #                 mkstream=True
# # #             )
# # #         except redis.exceptions.ResponseError:
# # #             # Group already exists
# # #             pass

# # #     # ---------------- PRODUCER ----------------
# # #     def enqueue_plan(self, task_id: str, steps):
# # #         """
# # #         Manual batching:
# # #         - Group steps by agent
# # #         - Push ONE message per agent
# # #         """
# # #         batches = defaultdict(list)

# # #         for step in steps:
# # #             batches[step.agent].append({
# # #                 "step_id": step.step_id,
# # #                 "payload": step.payload
# # #             })

# # #         for agent, agent_steps in batches.items():
# # #             message = {
# # #                 "task_id": task_id,
# # #                 "agent": agent,
# # #                 "steps": json.dumps(agent_steps)
# # #             }

# # #             self.client.xadd(self.stream_name, message)

# # #     # ---------------- CONSUMER ----------------
# # #     def consume(self, consumer_name: str):
# # #         return self.client.xreadgroup(
# # #             groupname=self.group_name,
# # #             consumername=consumer_name,
# # #             streams={self.stream_name: ">"},
# # #             count=1,
# # #             block=5000,
# # #         )

# # #     def ack(self, message_id: str):
# # #         self.client.xack(self.stream_name, self.group_name, message_id)




# # # import json

# # # EVENT_STREAM = "task_events"

# # # class RedisQueue:
# # #     # existing code stays

# # #     def emit_event(self, event: dict):
# # #         """
# # #         Push streaming event
# # #         """
# # #         self.client.xadd(EVENT_STREAM, {
# # #             "data": json.dumps(event)
# # #         })

# # #     def consume_events(self, last_id: str = "0"):
# # #         """
# # #         Read streaming events for SSE
# # #         """
# # #         return self.client.xread(
# # #             streams={EVENT_STREAM: last_id},
# # #             block=5000,
# # #             count=10
# # #         )






# # import redis
# # import json
# # from collections import defaultdict
# # from app.config import REDIS_HOST, REDIS_PORT

# # TASK_STREAM = "agent_tasks"
# # EVENT_STREAM = "task_events"
# # GROUP_NAME = "agent_workers"


# # class RedisQueue:
# #     def __init__(self):
# #         self.client = redis.Redis(
# #             host=REDIS_HOST,
# #             port=REDIS_PORT,
# #             decode_responses=True,
# #         )

# #         # Create consumer group for task stream
# #         try:
# #             self.client.xgroup_create(
# #                 name=TASK_STREAM,
# #                 groupname=GROUP_NAME,
# #                 id="0",
# #                 mkstream=True
# #             )
# #         except redis.exceptions.ResponseError:
# #             pass

# #     # -------- PRODUCER (TASKS) --------
# #     def enqueue_plan(self, task_id: str, steps):
# #         batches = defaultdict(list)

# #         for step in steps:
# #             batches[step.agent].append({
# #                 "step_id": step.step_id,
# #                 "payload": step.payload
# #             })

# #         for agent, agent_steps in batches.items():
# #             self.client.xadd(
# #                 TASK_STREAM,
# #                 {
# #                     "task_id": task_id,
# #                     "agent": agent,
# #                     "steps": json.dumps(agent_steps)
# #                 }
# #             )

# #     # -------- CONSUMER (TASKS) --------
# #     def consume(self, consumer_name: str):
# #         return self.client.xreadgroup(
# #             groupname=GROUP_NAME,
# #             consumername=consumer_name,
# #             streams={TASK_STREAM: ">"},
# #             count=1,
# #             block=5000,
# #         )

# #     def ack(self, message_id: str):
# #         self.client.xack(TASK_STREAM, GROUP_NAME, message_id)

# #     # -------- EVENTS (STREAMING) --------
# #     def emit_event(self, event: dict):
# #         self.client.xadd(
# #             EVENT_STREAM,
# #             {"data": json.dumps(event)}
# #         )

# #     def consume_events(self, last_id: str):
# #         return self.client.xread(
# #             streams={EVENT_STREAM: last_id},
# #             block=5000,
# #             count=10
# #         )
# #     def reenqueue_step(self, task_id: str, agent: str, step):
# #         self.client.xadd(
# #             TASK_STREAM,
# #             {
# #                 "task_id": task_id,
# #                 "agent": agent,
# #                 "steps": json.dumps([step])
# #             }
# #         )



# import redis
# import json
# from collections import defaultdict

# TASK_STREAM = "agent_tasks"
# EVENT_STREAM = "task_events"
# GROUP = "agent_workers"


# class RedisQueue:
#     def __init__(self):
#         self.client = redis.Redis(host="localhost", port=6379, decode_responses=True)
#         try:
#             self.client.xgroup_create(TASK_STREAM, GROUP, id="0", mkstream=True)
#         except redis.exceptions.ResponseError:
#             pass

#     # ---------- TASKS ----------
#     def enqueue_plan(self, task_id, steps):
#         batches = defaultdict(list)
#         for step in steps:
#             batches[step.agent].append({
#                 "step_id": step.step_id,
#                 "payload": step.payload,
#             })

#         for agent, agent_steps in batches.items():
#             self.client.xadd(
#                 TASK_STREAM,
#                 {
#                     "task_id": task_id,
#                     "agent": agent,
#                     "steps": json.dumps(agent_steps),
#                 }
#             )

#     def consume(self, consumer):
#         return self.client.xreadgroup(
#             GROUP, consumer, {TASK_STREAM: ">"}, block=5000
#         )

#     def ack(self, message_id):
#         self.client.xack(TASK_STREAM, GROUP, message_id)

#     def reenqueue_step(self, task_id, agent, step):
#         self.client.xadd(
#             TASK_STREAM,
#             {
#                 "task_id": task_id,
#                 "agent": agent,
#                 "steps": json.dumps([step]),
#             }
#         )

#     # ---------- EVENTS ----------
#     def emit_event(self, event):
#         self.client.xadd(EVENT_STREAM, {"data": json.dumps(event)})

#     def consume_events(self, last_id="0"):
#         return self.client.xread({EVENT_STREAM: last_id}, block=5000)


import redis
import json
from collections import defaultdict

TASK_STREAM = "agent_tasks"
EVENT_STREAM = "task_events"
GROUP = "agent_workers"
METRICS_PREFIX = "task_metrics:"

class RedisQueue:
    def __init__(self):
        self.r = redis.Redis(host="localhost", port=6379, decode_responses=True)
        try:
            self.r.xgroup_create(TASK_STREAM, GROUP, id="0", mkstream=True)
        except redis.exceptions.ResponseError:
            pass

    # ---------- TASK QUEUE ----------
    def enqueue_plan(self, task_id, steps):
        batches = defaultdict(list)
        for step in steps:
            batches[step.agent].append(step.dict())

        for agent, batch in batches.items():
            self.r.xadd(
                TASK_STREAM,
                {
                    "task_id": task_id,
                    "agent": agent,
                    "steps": json.dumps(batch),
                }
            )

    def consume(self, consumer):
        return self.r.xreadgroup(
            GROUP, consumer, {TASK_STREAM: ">"}, block=5000
        )

    def ack(self, msg_id):
        self.r.xack(TASK_STREAM, GROUP, msg_id)

    # ---------- EVENTS ----------
    def emit_event(self, event: dict):
        self.r.xadd(EVENT_STREAM, {"data": json.dumps(event)})

    def consume_events(self, last_id="0"):
        return self.r.xread({EVENT_STREAM: last_id}, block=5000)

    # ---------- METRICS ----------
    def store_metrics(self, task_id: str, metrics: dict):
        self.r.set(f"{METRICS_PREFIX}{task_id}", json.dumps(metrics))

    def get_metrics(self, task_id: str):
        data = self.r.get(f"{METRICS_PREFIX}{task_id}")
        return json.loads(data) if data else None
