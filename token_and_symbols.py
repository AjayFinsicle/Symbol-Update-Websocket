# import asyncio
# import websockets
# import json

# token_symbol_map = {} 

# async def handle_websocket_connection(websocket, path):
#     try:
#         async for message in websocket:
#             # Handle messages received from clients (React or Python)
#             print(f"Received message: {message}")

#             # Parse the JSON message
#             data = json.loads(message)

#             if data.get("type") == "code_response":
#                 access_token = data.get("token")
#                 symbols = data.get("symbols")
                
#                 # Store the access token and symbols in the dictionary
#                 token_symbol_map[access_token] = symbols
#                 print("--------------------------------------------------")
#                 print("Token Symbols map", token_symbol_map)

#     except websockets.exceptions.ConnectionClosedError:
#         pass

# start_server = websockets.serve(handle_websocket_connection, "localhost", 8999)  # You can use your desired host and port

# if __name__ == "__main__":
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()



