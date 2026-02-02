# # # print(">>> agent_worker.py LOADED <<<", flush=True)

# # # import sys
# # # import json
# # # from datetime import datetime
# # # from app.queue.redis_queue import RedisQueue
# # # from app.agents import retriever, analyzer, writer


# # # AGENT_MAP = {
# # #     "retriever": retriever,
# # #     "analyzer": analyzer,
# # #     "writer": writer,
# # # }


# # # def log(message: str):
# # #     print(
# # #         f"[{datetime.utcnow().strftime('%H:%M:%S')}] [WORKER] {message}",
# # #         flush=True
# # #     )


# # # def main():
# # #     log("Worker starting (handles ALL agents)")

# # #     queue = RedisQueue()
# # #     consumer = "main_worker"

# # #     log("Connected to Redis, waiting for task batches...")

# # #     while True:
# # #         messages = queue.consume(consumer)

# # #         if not messages:
# # #             continue

# # #         for _, entries in messages:
# # #             for message_id, data in entries:
# # #                 agent = data["agent"]
# # #                 steps = json.loads(data["steps"])

# # #                 log(f"Received batch {message_id} for agent '{agent}'")

# # #                 if agent not in AGENT_MAP:
# # #                     log(f"Unknown agent '{agent}', skipping batch")
# # #                     queue.ack(message_id)
# # #                     continue

# # #                 for step in steps:
# # #                     step_id = step["step_id"]
# # #                     payload = step["payload"]

# # #                     log(f"Running {agent} step {step_id}")
# # #                     result = AGENT_MAP[agent].run(payload)
# # #                     log(f"Result: {result}")

# # #                 queue.ack(message_id)
# # #                 log(f"ACKED batch {message_id}\n")


# # # if __name__ == "__main__":
# # #     main()


# # print(">>> agent_worker.py LOADED <<<", flush=True)

# # import json
# # from datetime import datetime
# # from app.queue.redis_queue import RedisQueue
# # from app.agents import retriever, analyzer, writer


# # AGENT_MAP = {
# #     "retriever": retriever,
# #     "analyzer": analyzer,
# #     "writer": writer,
# # }


# # def log(msg):
# #     print(
# #         f"[{datetime.utcnow().strftime('%H:%M:%S')}] [WORKER] {msg}",
# #         flush=True
# #     )


# # def main():
# #     queue = RedisQueue()
# #     consumer = "main_worker"

# #     log("Worker started (handles all agents)")

# #     while True:
# #         messages = queue.consume(consumer)

# #         if not messages:
# #             continue

# #         for _, entries in messages:
# #             for message_id, data in entries:
# #                 agent = data["agent"]
# #                 steps = json.loads(data["steps"])

# #                 log(f"Received batch {message_id} for agent {agent}")

# #                 for step in steps:
# #                     step_id = step["step_id"]
# #                     payload = step["payload"]

# #                     # ---- STREAM: STEP STARTED ----
# #                     queue.emit_event({
# #                         "event": "step_started",
# #                         "agent": agent,
# #                         "step_id": step_id
# #                     })

# #                     log(f"Running {agent} step {step_id}")
# #                     result = AGENT_MAP[agent].run(payload)

# #                     # ---- STREAM: STEP COMPLETED ----
# #                     queue.emit_event({
# #                         "event": "step_completed",
# #                         "agent": agent,
# #                         "step_id": step_id,
# #                         "result": result
# #                     })

# #                 queue.ack(message_id)
# #                 log(f"ACKED batch {message_id}")


# # if __name__ == "__main__":
# #     main()


# print(">>> agent_worker.py LOADED <<<", flush=True)

# import json
# from app.queue.redis_queue import RedisQueue
# from app.agents import retriever, analyzer, writer
# from app.utils.logger import log
# from app.utils.retry import should_retry


# AGENT_MAP = {
#     "retriever": retriever,
#     "analyzer": analyzer,
#     "writer": writer,
# }


# def main():
#     queue = RedisQueue()
#     consumer = "main_worker"

#     log("Worker started with retries + streaming enabled")

#     while True:
#         messages = queue.consume(consumer)

#         if not messages:
#             continue

#         for _, entries in messages:
#             for message_id, data in entries:
#                 agent = data["agent"]
#                 steps = json.loads(data["steps"])
#                 task_id = data["task_id"]

#                 log(
#                     message=f"Received batch {message_id}",
#                     agent=agent,
#                     task_id=task_id
#                 )

#                 for step in steps:
#                     step_id = step["step_id"]
#                     payload = step["payload"]
#                     retry_count = step.get("retry", 0)

#                     # ---- STREAM: STEP STARTED ----
#                     queue.emit_event({
#                         "event": "step_started",
#                         "agent": agent,
#                         "step_id": step_id,
#                         "retry": retry_count
#                     })

#                     try:
#                         log(
#                             message=f"Running step {step_id} (retry={retry_count})",
#                             agent=agent,
#                             task_id=task_id
#                         )

#                         result = AGENT_MAP[agent].run(payload)

#                         # ---- STREAM: STEP COMPLETED ----
#                         queue.emit_event({
#                             "event": "step_completed",
#                             "agent": agent,
#                             "step_id": step_id,
#                             "result": result
#                         })

#                         log(
#                             message=f"Step {step_id} completed",
#                             agent=agent,
#                             task_id=task_id
#                         )

#                     except Exception as e:
#                         log(
#                             message=f"Error in step {step_id}: {e}",
#                             level="ERROR",
#                             agent=agent,
#                             task_id=task_id
#                         )

#                         retry_count += 1

#                         if should_retry(retry_count):
#                             step["retry"] = retry_count

#                             queue.emit_event({
#                                 "event": "step_retried",
#                                 "agent": agent,
#                                 "step_id": step_id,
#                                 "retry": retry_count
#                             })

#                             log(
#                                 message=f"Retrying step {step_id} (retry={retry_count})",
#                                 level="WARN",
#                                 agent=agent,
#                                 task_id=task_id
#                             )

#                             queue.reenqueue_step(task_id, agent, step)

#                         else:
#                             queue.emit_event({
#                                 "event": "step_failed",
#                                 "agent": agent,
#                                 "step_id": step_id
#                             })

#                             log(
#                                 message=f"Step {step_id} permanently failed",
#                                 level="ERROR",
#                                 agent=agent,
#                                 task_id=task_id
#                             )

#                 queue.ack(message_id)
#                 log(
#                     message=f"ACKED batch {message_id}",
#                     agent=agent,
#                     task_id=task_id
#                 )


# if __name__ == "__main__":
#     main()


print(">>> AGENT WORKER LOADED <<<", flush=True)

import json
import time
from app.queue.redis_queue import RedisQueue
from app.utils.logger import log
from app.utils.metrics import TaskMetrics
from app.agents import retriever, analyzer, writer

AGENT_IMPL = {
    "retriever": retriever,
    "analyzer": analyzer,
    "writer": writer,
}

def main():
    queue = RedisQueue()
    consumer = "worker-1"

    log("WORKER started and waiting for tasks")

    while True:
        messages = queue.consume(consumer)

        if not messages:
            log("WORKER idle (no tasks)", level="DEBUG")
            time.sleep(2)
            continue

        for _, entries in messages:
            for msg_id, data in entries:
                task_id = data["task_id"]
                agent = data["agent"]
                steps = json.loads(data["steps"])

                log(
                    f"DISPATCHED → {agent.upper()} (batch size={len(steps)})",
                    agent=agent,
                    task_id=task_id,
                )

                metrics = TaskMetrics(task_id)

                for step in steps:
                    step_id = step["step_id"]

                    log(
                        f"STEP {step_id} STARTED",
                        agent=agent,
                        task_id=task_id,
                    )

                    queue.emit_event({
                        "event": "step_started",
                        "task_id": task_id,
                        "agent": agent,
                        "step_id": step_id,
                    })

                    result = AGENT_IMPL[agent].run(step["payload"])
                    metrics.add_cost(agent)

                    log(
                        f"STEP {step_id} COMPLETED",
                        agent=agent,
                        task_id=task_id,
                    )

                    queue.emit_event({
                        "event": "step_completed",
                        "task_id": task_id,
                        "agent": agent,
                        "step_id": step_id,
                        "result": result,
                    })

                    if agent == "writer":
                        final_metrics = metrics.finish(result)

                        log(
                            "TASK COMPLETED END-TO-END",
                            agent="writer",
                            task_id=task_id,
                        )

                        queue.emit_event({
                            "event": "task_completed",
                            "task_id": task_id,
                            "metrics": final_metrics,
                        })

                queue.ack(msg_id)
                log("BATCH ACKED", agent=agent, task_id=task_id)

if __name__ == "__main__":
    main()
