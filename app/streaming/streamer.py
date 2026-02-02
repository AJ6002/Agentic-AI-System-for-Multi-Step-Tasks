# # # import redis
# # # import json
# # # from fastapi.responses import StreamingResponse
# # # from app.config import REDIS_HOST, REDIS_PORT, EVENT_STREAM


# # # def stream_events():
# # #     client = redis.Redis(
# # #         host=REDIS_HOST,
# # #         port=REDIS_PORT,
# # #         decode_responses=True,
# # #     )
# # #     last_id = "0"

# # #     while True:
# # #         events = client.xread({EVENT_STREAM: last_id}, block=5000)
# # #         for _, messages in events:
# # #             for msg_id, data in messages:
# # #                 last_id = msg_id
# # #                 yield f"data: {data['data']}\n\n"


# # import json
# # import time
# # from app.queue.redis_queue import RedisQueue


# # def stream_events():
# #     """
# #     Server-Sent Events generator
# #     """
# #     queue = RedisQueue()
# #     last_id = "0"

# #     while True:
# #         events = queue.consume_events(last_id)

# #         if not events:
# #             time.sleep(0.5)
# #             continue

# #         for _, messages in events:
# #             for event_id, event_data in messages:
# #                 last_id = event_id
# #                 payload = json.loads(event_data["data"])

# #                 yield f"data: {json.dumps(payload)}\n\n"




# import json
# import time
# from app.queue.redis_queue import RedisQueue

# def stream_task(task_id, replay=False):
#     queue = RedisQueue()
#     last_id = "0"
#     buffer = []

#     while True:
#         events = queue.consume_events(last_id)

#         if not events:
#             time.sleep(0.3)
#             continue

#         for _, messages in events:
#             for event_id, raw in messages:
#                 last_id = event_id
#                 event = json.loads(raw["data"])

#                 if event.get("task_id") != task_id:
#                     continue

#                 buffer.append(event)
#                 yield f"data: {json.dumps(event)}\n\n"

#                 if event["event"] == "task_completed":
#                     if replay:
#                         time.sleep(1)
#                         for e in buffer:
#                             yield f"data: {json.dumps(e)}\n\n"
#                     return

import json, time
from app.queue.redis_queue import RedisQueue

def stream_task(task_id, replay=False):
    queue = RedisQueue()
    last_id = "0"
    history = []

    while True:
        events = queue.consume_events(last_id)

        if not events:
            time.sleep(0.3)
            continue

        for _, messages in events:
            for eid, raw in messages:
                last_id = eid
                event = json.loads(raw["data"])

                if event.get("task_id") != task_id:
                    continue

                history.append(event)
                yield f"data: {json.dumps(event)}\n\n"

                if event["event"] == "task_completed":
                    if replay:
                        for e in history:
                            yield f"data: {json.dumps(e)}\n\n"
                    return
