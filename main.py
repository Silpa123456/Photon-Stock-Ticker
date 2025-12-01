# main.py
from fastapi import FastAPI, WebSocket
import asyncio
import random
import json

app = FastAPI()


class ConnectionManager:
    """
    Keeps track of all connected clients and sends
    stock updates to everyone.
    """
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # Send message to all connected clients
        disconnected = []
        for ws in self.active_connections:
            try:
                await ws.send_text(message)
            except Exception:
                # If sending fails, mark it as disconnected
                disconnected.append(ws)
        for ws in disconnected:
            self.disconnect(ws)


manager = ConnectionManager()

# some fake starting prices
TICKERS = {
    "AAPL": 150.0,
    "GOOGL": 2800.0,
    "TSLA": 700.0,
    "MSFT": 320.0,
}


async def stock_price_generator():
    """
    Generates fake stock prices forever and broadcasts
    them to all connected clients every second.
    """
    while True:
        for name, price in list(TICKERS.items()):
            # random price change between -2 and +2
            change = random.uniform(-2, 2)
            new_price = max(1, price + change)
            new_price = round(new_price, 2)
            TICKERS[name] = new_price

            data = {
                "ticker": name,
                "price": new_price,
            }

            # send as JSON string
            await manager.broadcast(json.dumps(data))
            await asyncio.sleep(1)


@app.on_event("startup")
async def start_generator():
    # start background task when server starts
    asyncio.create_task(stock_price_generator())


@app.websocket("/ws/stocks")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that clients connect to.
    They only receive messages (no need to send).
    """
    await manager.connect(websocket)
    try:
        # keep connection alive
        while True:
            await asyncio.sleep(60)
    finally:
        manager.disconnect(websocket)


# To run: uvicorn main:app --reload
