import asyncio
import websockets
from fyers_apiv3.FyersWebsocket import data_ws
import json

# Create a set to keep track of subscribed symbols
subscribed_symbols = set()

socket_symbols_map = {}
fyers_instance = None

def onmessage(message):
    try:
        symbol_data = message
        print(symbol_data)
        messege_send(symbol_data, socket_symbols_map)
    except KeyError as e:
        print("KeyError:", e)

def messege_send(symbol_data, socket_symbols_map):
    print("Sending message: ", symbol_data)
    print("Socket Symbols Map in messege_send: ", socket_symbols_map)

    for socket_id, symbols in socket_symbols_map.items():
        if symbol_data["symbol"] in symbols:
            socket_data = (socket_id, symbol_data)
            # messege_send_to_client(socket_data)
            print(f"Data for Socket ID {socket_id}: {symbol_data}")

# def messege_send_to_client(socket_data):
#     socket_id, symbol_data = socket_data
#     # Assuming you have the WebSocket URL, replace 'ws://example.com' with your actual WebSocket URL
#     ws_url = 'ws://localhost:9999'
    
#     # Create a WebSocket connection
#     ws = websockets.create_connection(ws_url)
#     ws.send(symbol_data)
#     ws.close()


def onerror(message):
    print("Error:", message)

def onclose():
    print("Connection closed")

def onopen():
    print("WebSocket connection opened")

async def listen_to_external_websocket(websocket, path):
    global socket_symbols_map 
    global fyers_instance 

    while True:
        try:
            # Wait for a message from the WebSocket
            message = await websocket.recv()
            print(f"Received message: {message}")

            # Extract access token, symbols, socket IDs, and socket-symbols map from the received message
            access_token, symbols, socket_ids, _ = extract_data_from_message(message)

            # Subscribe to symbols using the received access token
            if access_token and symbols:
                print(f"Received access token: {access_token}")
                print(f"Received symbols: {symbols}")

                # Organize symbols for each socket_id
                new_socket_symbols_map = {}
                for i, socket_id in enumerate(socket_ids):
                    start_index = i * 3
                    end_index = start_index + 3
                    symbols_for_socket = symbols[start_index:end_index]
                    print(f"Socket ID {socket_id}: {symbols_for_socket}")
                    new_socket_symbols_map[socket_id] = symbols_for_socket

                # Check if the socket_id is already in socket_symbols_map
                for socket_id, new_symbols in new_socket_symbols_map.items():
                    if socket_id in socket_symbols_map:
                        # Check if the new symbols are different from the existing ones
                        if set(new_symbols) != set(socket_symbols_map[socket_id]):
                            # Unsubscribe old symbols for that socket_id
                            symbols_to_unsubscribe = set(socket_symbols_map[socket_id]) - set(new_symbols)
                            for symbol in symbols_to_unsubscribe:
                                print(f"Unsubscribing from {symbol} for Socket ID {socket_id}")
                                # Unsubscribe old symbol for that particular socket id
                                fyers_instance.unsubscribe(symbols=[symbol])
                                socket_symbols_map[socket_id].remove(symbol)
                            # Subscribe new symbols for that socket_id
                            for symbol in new_symbols:
                                print(f"Subscribing to {symbol} for Socket ID {socket_id}")
                                fyers_instance.subscribe(symbols=[symbol], data_type="SymbolUpdate")
                                socket_symbols_map[socket_id].append(symbol)
                    else:
                        # If the socket_id is not in socket_symbols_map, simply add it
                        socket_symbols_map[socket_id] = new_symbols

                # Print updated socket-symbols map
                print(f"Updated Socket Symbols Map: {socket_symbols_map}")

                # Subscribe to symbols using the received access token
                subscribe_to_symbols(access_token, symbols)

        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed. Reconnecting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def extract_data_from_message(message):
    try:
        # Assuming message is a JSON-formatted list
        data_list = json.loads(message)

        access_token = None
        symbols = []
        socket_ids = []

        for data in data_list:
            if "type" in data and data["type"] == "code_response":
                access_token = data.get("token")
                symbols.extend(data.get("symbols", []))
                socket_id = data.get("socket_id")
                socket_ids.append(socket_id)

        # Create a dictionary to map socket IDs to symbols
        socket_symbols_map = {socket_id: symbols for socket_id in socket_ids}

        if access_token and symbols:
            return access_token, symbols, socket_ids, socket_symbols_map

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    return None, None, None, None

def subscribe_to_symbols(access_token, symbols):
    global subscribed_symbols  # Declare subscribed_symbols as global
    global fyers_instance  # Declare fyers_instance as global

    # Create a new FyersDataSocket instance with the received access token
    fyers_instance = create_fyers_instance(access_token)
    fyers_instance.connect()

    # Subscribe to the union of old and new symbols
    all_symbols = subscribed_symbols.union(set(symbols))

    # Unsubscribe from symbols that are no longer present
    symbols_to_unsubscribe = subscribed_symbols - set(all_symbols)
    for symbol in symbols_to_unsubscribe:
        if symbol in subscribed_symbols:
            print(f"Unsubscribing from {symbol}")
            fyers_instance.unsubscribe(symbols=[symbol])
            subscribed_symbols.discard(symbol)

    # Subscribe to all symbols
    for symbol in all_symbols:
        data_type = "SymbolUpdate"
        print(f"Subscribing to {symbol}")
        fyers_instance.subscribe(symbols=[symbol], data_type=data_type)
        subscribed_symbols.add(symbol)

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
