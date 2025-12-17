from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI()

MESSAGES = []
MAX_MESSAGES = 200


@app.get("/")
def root():
    return {"status": "ok"}   # <- REQUIRED for Railway


class Message(BaseModel):
    room: str
    user: str
    payload: str
    ts: float | None = None


@app.post("/send")
def send(msg: Message):
    msg.ts = time.time()
    MESSAGES.append(msg.dict())
    if len(MESSAGES) > MAX_MESSAGES:
        MESSAGES.pop(0)
    return {"ok": True}


@app.get("/poll")
def poll(room: str, after: float = 0):
    return [
        m for m in MESSAGES
        if m["room"] == room and m["ts"] > after
    ]

import threading, time
threading.Thread(target=lambda: time.sleep(10**9), daemon=False).start()


