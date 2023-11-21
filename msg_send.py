import asyncio
import websockets
import json

async def send_test_messages():
    async with websockets.connect("ws://localhost:9999") as websocket:
        test_message = [
            {
                "type": "code_response",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTkyNDg5MjYsImV4cCI6MTY5OTMxNzAyNiwibmJmIjoxNjk5MjQ4OTI2LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbFNIc2U3em80TVFZSTZaZDNWekJKSzRtRjlhdzZXV0pOWVBuWVlDRGpyZzFNZnVyVEg3Yy1NQmNRa1NiRWl3YlBDTEJiNXB5dkN1cmtDYVMtckhVa0pKNFEwRmJOTVpXSDZLRGotWFk3ZExUcTlxbz0iLCJkaXNwbGF5X25hbWUiOiJGSU5TSUNMRSBQUklWQVRFIExJTUlURUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI4OGE2NzUwYjc4ZmNiNWI2NGZhOWVlZTQ2NTlkZTVkZDFhY2M0MWFmNzJiOWZlNWU1MDBhYTg0NyIsImZ5X2lkIjoiQ0EwMDEzOCIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.JPGdUbTHDwS5EzJEh8kxMrPutmSFd0t-bKjGGdMXpAU",
                "symbols": ["NSE:NIFTY50-INDEX"],
            },
            {
                "type":"code_response",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTkyNDkwOTUsImV4cCI6MTY5OTMxNzAxNSwibmJmIjoxNjk5MjQ5MDk1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbFNIdkhobi1BakdSQUk5cWFseEZPOGpKcDRBbVFKQUxDQUxobFRTbXBUNVhSMllpZ2JLRjFTQzMwTGNoS25hVEZJNi0yUDJBMDJKdHVIY3hodU5ZcEkzdlNkNWQ1NG5DZjZmTXBTVkdUWU5ZNHIyND0iLCJkaXNwbGF5X25hbWUiOiJGSU5TSUNMRSBQUklWQVRFIExJTUlURUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI4OGE2NzUwYjc4ZmNiNWI2NGZhOWVlZTQ2NTlkZTVkZDFhY2M0MWFmNzJiOWZlNWU1MDBhYTg0NyIsImZ5X2lkIjoiQ0EwMDEzOCIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.Ebd0F9h5gcW1nV3QHalkjym5CKQnL41eBEKIR5JuNpw",
                "symbols": ["NSE:FINNIFTY-INDEX"],

            }
        ]

        # Send the test message
        await websocket.send(json.dumps(test_message))

# Run the WebSocket client to send test messages
asyncio.get_event_loop().run_until_complete(send_test_messages())



# import asyncio
# import websockets
# import json

# async def generate_test_message(token, symbols):
#     return [
#         {
#             "type": "code_response",
#             "token": token,
#             "symbols": symbols,
#         }
#     ]

# async def send_test_messages():
#     async with websockets.connect("ws://localhost:8999") as websocket:
#         # You can dynamically generate test messages with different values
#         message1 = await generate_test_message("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTkyNDg5MjYsImV4cCI6MTY5OTMxNzAyNiwibmJmIjoxNjk5MjQ4OTI2LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbFNIc2U3em80TVFZSTZaZDNWekJKSzRtRjlhdzZXV0pOWVBuWVlDRGpyZzFNZnVyVEg3Yy1NQmNRa1NiRWl3YlBDTEJiNXB5dkN1cmtDYVMtckhVa0pKNFEwRmJOTVpXSDZLRGotWFk3ZExUcTlxbz0iLCJkaXNwbGF5X25hbWUiOiJGSU5TSUNMRSBQUklWQVRFIExJTUlURUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI4OGE2NzUwYjc4ZmNiNWI2NGZhOWVlZTQ2NTlkZTVkZDFhY2M0MWFmNzJiOWZlNWU1MDBhYTg0NyIsImZ5X2lkIjoiQ0EwMDEzOCIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.JPGdUbTHDwS5EzJEh8kxMrPutmSFd0t-bKjGGdMXpAU", ["NSE:BANKNIFTY-INDEX"])
#         message2 = await generate_test_message("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTkyNDkwOTUsImV4cCI6MTY5OTMxNzAxNSwibmJmIjoxNjk5MjQ5MDk1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbFNIdkhobi1BakdSQUk5cWFseEZPOGpKcDRBbVFKQUxDQUxobFRTbXBUNVhSMllpZ2JLRjFTQzMwTGNoS25hVEZJNi0yUDJBMDJKdHVIY3hodU5ZcEkzdlNkNWQ1NG5DZjZmTXBTVkdUWU5ZNHIyND0iLCJkaXNwbGF5X25hbWUiOiJGSU5TSUNMRSBQUklWQVRFIExJTUlURUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI4OGE2NzUwYjc4ZmNiNWI2NGZhOWVlZTQ2NTlkZTVkZDFhY2M0MWFmNzJiOWZlNWU1MDBhYTg0NyIsImZ5X2lkIjoiQ0EwMDEzOCIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.Ebd0F9h5gcW1nV3QHalkjym5CKQnL41eBEKIR5JuNpw", ["NSE:NIFTY50-INDEX"])

#         # Print the messages before sending
#         print("Sending Message 1:", json.dumps(message1))
#         await websocket.send(json.dumps(message1))
#         print("Sending Message 2:", json.dumps(message2))
#         await websocket.send(json.dumps(message2))

# # Run the WebSocket client to send test messages
# asyncio.get_event_loop().run_until_complete(send_test_messages())
