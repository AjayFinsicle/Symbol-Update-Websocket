import asyncio
import websockets
import json

async def send_message():
    uri = "ws://localhost:8999"  # Replace with the actual address and port of your WebSocket server

    async with websockets.connect(uri) as websocket:
        # Prepare the message as a JSON-formatted list
        message_data = [
            {"type": "code_response", "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MDA2MzE0MTAsImV4cCI6MTcwMDY5OTQ1MCwibmJmIjoxNzAwNjMxNDEwLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbFhaTnlMQXg3SG5abFozeUNRdWhELUxYZVRfWklkSnlCM1FHX1NBSTRXSi02Z3hpc1hjYnFzVEFOTkVWMGlCWkl5ZkpfSnNiYWRoTlBQbnlfV1daSGRuX0NXbktFMzVzMWFmYjlILUtYZmJYekhmUT0iLCJkaXNwbGF5X25hbWUiOiJGSU5TSUNMRSBQUklWQVRFIExJTUlURUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI4OGE2NzUwYjc4ZmNiNWI2NGZhOWVlZTQ2NTlkZTVkZDFhY2M0MWFmNzJiOWZlNWU1MDBhYTg0NyIsImZ5X2lkIjoiQ0EwMDEzOCIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.wr83zXH80IvrALBY9LgahUY2dXZo8ukz08NSWVZLWoQ", "symbols": ["NSE:FINNIFTY-INDEX"], "socket_id": "001"}
            # Add more data as needed
        ]

        # Convert the data to JSON and send it to the server
        message = json.dumps(message_data)
        await websocket.send(message)
        print(f"Message sent: {message}")

# Run the script to send the message
asyncio.get_event_loop().run_until_complete(send_message())
