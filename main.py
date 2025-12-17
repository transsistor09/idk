from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI()

MESSAGES = []
MAX_MESSAGES = 200


@app.get("/")
def root():
    return "ok"

class Message(BaseModel):
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
def poll(after: float = 0):
    return [m for m in MESSAGES if m["ts"] > after]


