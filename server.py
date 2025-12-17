# server.py
import os
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
connections = []

# Allow any origin for WebSocket / CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok"}  # prevents 499 on GET /

@app.websocket("/ws")
async def chat(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    try:
        while True:
            data = await ws.receive_text()
            # Broadcast to all except sender
            for conn in connections:
                if conn != ws:
                    await conn.send_text(data)
    except:
        connections.remove(ws)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway sets PORT automatically
    uvicorn.run(app, host="0.0.0.0", port=port)
