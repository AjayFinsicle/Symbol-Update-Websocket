import asyncio
import websockets
import json

async def receive_data():
    uri = "ws://localhost:8999"  # Change this to match your WebSocket server address

    async with websockets.connect(uri) as websocket:
        print("WebSocket connection established.")

        try:
            while True:
                message = await websocket.recv()
                print(f"Received raw message: {message}")

                try:
                    data = json.loads(message)
                    print(f"Received data for Socket ID {data[0]}: {data[1]}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(receive_data())
