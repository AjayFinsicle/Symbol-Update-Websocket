import asyncio
import websockets
from fyers_apiv3.FyersWebsocket import data_ws
import json

# Create a dictionary to keep track of subscribed symbols for each device
device_symbols = {}

def onmessage(message):
    try:
        symbol_data = message
        print(symbol_data)
        # Process and handle the data for the specific symbol here
    except KeyError as e:
        print("KeyError:", e)

def onerror(message):
    print("Error:", message)

def onclose():
    print("Connection closed")

def onopen():
    print("WebSocket connection opened")

async def listen_to_external_websocket(websocket, path):
    while True:
        try:
            # Wait for a message from the WebSocket
            message = await websocket.recv()
            print(f"Received message: {message}")

            # Extract access token, symbols, and device_id from the received message
            result = extract_data_from_message(message)

            # Subscribe to symbols using the received access token
            if result:
                access_token, symbols, device_id = result
                print(f"Received access token: {access_token}")
                print(f"Received symbols: {symbols}")
                print(f"Received device ID: {device_id}")

                # Subscribe to symbols using the received access token for the specific device
                subscribe_to_symbols(access_token, symbols, device_id)

        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed. Reconnecting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def extract_data_from_message(message):
    try:
        # Assuming message is a JSON-formatted list
        data_list = json.loads(message)

        for data in data_list:
            if "type" in data and data["type"] == "code_response":
                access_token = data.get("token")
                symbols = data.get("symbols", [])
                device_id = data.get("socket_id")

                if access_token and symbols and device_id:
                    return access_token, symbols, device_id

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    return None, None, None


def subscribe_to_symbols(access_token, symbols, device_id):
    if device_id not in device_symbols:
        device_symbols[device_id] = set()

    # Create a new FyersDataSocket instance with the received access token for the specific device
    fyers_instance = create_fyers_instance(access_token)
    fyers_instance.connect()

    # Unsubscribe from old symbols for the specific device
    symbols_to_unsubscribe = device_symbols[device_id] - set(symbols)
    for symbol in symbols_to_unsubscribe:
        if symbol in device_symbols[device_id]:
            print(f"Unsubscribing from {symbol} for device {device_id}")
            fyers_instance.unsubscribe(symbols=[symbol])
            device_symbols[device_id].discard(symbol)

    # Subscribe to new symbols for the specific device
    symbols_to_subscribe = set(symbols) - device_symbols[device_id]
    for symbol in symbols_to_subscribe:
        data_type = "SymbolUpdate"
        print(f"Subscribing to {symbol} for device {device_id}")
        fyers_instance.subscribe(symbols=[symbol], data_type=data_type)
        device_symbols[device_id].add(symbol)

def create_fyers_instance(access_token):
    return data_ws.FyersDataSocket(
        access_token=access_token,
        log_path="",
        litemode=False,
        write_to_file=False,
        reconnect=True,
        on_connect=onopen,
        on_close=onclose,
        on_error=onerror,
        on_message=onmessage
    )

# Specify the address and port for the WebSocket server
server_address = "localhost"
server_port = 8999

# Start the WebSocket server
start_server = websockets.serve(listen_to_external_websocket, server_address, server_port)

# Run the event loop to continuously listen to the WebSocket
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
