# from datetime import datetime

# def log(message, level="INFO", agent=None, task_id=None):
#     ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
#     parts = [ts, level]

#     if agent:
#         parts.append(f"agent={agent}")
#     if task_id:
#         parts.append(f"task_id={task_id}")

#     prefix = " | ".join(parts)
#     print(f"[{prefix}] {message}", flush=True)

from datetime import datetime

def log(message, level="INFO", agent=None, task_id=None):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    parts = [ts, level]

    if agent:
        parts.append(f"agent={agent}")
    if task_id:
        parts.append(f"task_id={task_id}")

    prefix = " | ".join(parts)
    print(f"[{prefix}] {message}", flush=True)
