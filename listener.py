import asyncio
import websockets

async def handle_websocket_connection(websocket, path):
    try:
        async for message in websocket:
            # Handle messages received from clients (React or Python)
            # print(f"Received message: {message}")
            response = message
            data = {}
            data.append(response)
            print(data)
    except websockets.exceptions.ConnectionClosedError:
        pass

start_server = websockets.serve(handle_websocket_connection, "localhost", 8999) 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()