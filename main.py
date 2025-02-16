from dotenv import load_dotenv

load_dotenv("./.env")
import asyncio
import json
import websockets
import threading
from langchain_openai import ChatOpenAI

from my_browser_use import agent

message_queue = (
    asyncio.Queue()
)  # Shared queue for websocket messages between async processes


async def process_queue(websocket):
    while True:
        message = await message_queue.get()
        await websocket.send(message)


async def websocket_handler(websocket):
    """Handles WebSocket connections and starts a background task to process messages."""
    asyncio.create_task(
        process_queue(websocket)
    )  # Run message processing independently
    try:
        while True:
            await asyncio.sleep(1)  # Keep connection alive
    except websockets.exceptions.ConnectionClosed:
        pass


async def websocket_server():
    """Starts the WebSocket server."""
    ws_server = await websockets.serve(websocket_handler, "localhost", 8765)
    await ws_server.serve_forever()


def start_websocket_thread():
    """Runs the WebSocket server in a separate thread."""
    asyncio.run(websocket_server())


def start_agent_thread():
    """Runs the agent in a separate thread."""
    asyncio.run(agent.main(message_queue))


async def main():
    await message_queue.put(json.dumps({"state": "INITIAL_STATE"}))
    """Runs agent.main() while WebSocket runs in another thread."""
    # Start WebSocket server in a separate thread
    websocket_thread = threading.Thread(target=start_websocket_thread, daemon=True)
    websocket_thread.start()

    # Run the agent process in the main event loop
    await agent.main(message_queue)


if __name__ == "__main__":
    asyncio.run(main())
