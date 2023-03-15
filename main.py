from collections import defaultdict, deque
from typing import Any, Optional

from fastapi import FastAPI

app = FastAPI()


queues = defaultdict(deque)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/queue/{queue_name}")
async def put_in_queue(queue_name: str, message: Any):
    queues[queue_name].append(message)
    return {"status": "ok"}


@app.get("/queue/{queue_name}", response_model=Optional[Any])
async def get_from_queue(queue_name: str):
    queue = queues[queue_name]
    return queue.popleft() if queue else None


@app.get("/count/{queue_name}", response_model=int)
async def count_queue(queue_name: str):
    return len(queues[queue_name])


@app.get("/enumerate/queues")
async def enumerate_queues():
    return list(queues.keys())
