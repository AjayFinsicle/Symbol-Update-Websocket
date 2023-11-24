from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit
import asyncio
import threading
import queue
import json
from aiohttp import web
from fyers_apiv3.FyersWebsocket import data_ws
from aiohttp import web
import requests
from threading import Thread

# Create a set to keep track of subscribed symbols
subscribed_symbols = set()

socket_symbols_map = {}
fyers_instance = None

# Create a thread-safe queue to pass messages between threads
message_queue = queue.Queue()

def onmessage(message):
    try:
        symbol_data = message
        print(symbol_data)
        message_queue.put(symbol_data)
    except KeyError as e:
        print("KeyError:", e)

# async def messege_send(symbol_data, socket_symbols_map):
#     print("Sending message: ", symbol_data)
#     print("Socket Symbols Map in messege_send: ", socket_symbols_map)

#     for socket_id, symbols in socket_symbols_map.items():
#         if symbol_data["symbol"] in symbols:
#             socket_data = (socket_id, symbol_data)
#             print(f"Data for Socket ID {socket_id}: {symbol_data}")
#             socketio_9999.emit('message', symbol_data, room=str(socket_id))
#             print(f"Data sent to Socket.IO for Socket ID {socket_id}")

async def messege_send(symbol_data, socket_symbols_map):
    print("Sending message: ", symbol_data)
    print("Socket Symbols Map in messege_send: ", socket_symbols_map)

    for socket_id, symbols in socket_symbols_map.items():
        print("udhudd")
        # Check if "symbol" key exists in symbol_data and if any word in symbols matches any word in symbol_data["symbol"]
        if "symbol" in symbol_data and any(word in symbol_data["symbol"] for word in symbols):
            socket_data = (socket_id, symbol_data)
            print(f"Data for Socket ID {socket_id}: {symbol_data}")
            socketio_9999.emit('message', symbol_data, room=str(socket_id))
            print(f"Data sent to Socket.IO for Socket ID {socket_id}")




def message_consumer():
    while True:
        try:
            # Get a message from the queue and run the messege_send coroutine
            message = message_queue.get()
            asyncio.run(messege_send(message, socket_symbols_map))
        except Exception as e:
            print(f"An error occurred in message_consumer: {e}")
            # print(f"An error occurred in message_consumer: {type(e)} - {e}")
            # print(f"Error source: {e.__traceback__}")
            # print(f"Message content: {message}")



# Start the message_consumer thread
consumer_thread = threading.Thread(target=message_consumer, daemon=True)
consumer_thread.start()

def onerror(message):
    print("Error:", message)

def onclose():
    print("Connection closed")

def onopen():
    print("WebSocket connection opened")

# def extract_data_from_message(message):
#     try:
#         # Assuming message is a JSON-formatted list
#         data_list = json.loads(message)

#         access_token = None
#         symbols = []
#         socket_ids = []

#         for data in data_list:
#             if "type" in data and data["type"] == "code_response":
#                 access_token = data.get("token")
#                 symbols.extend(data.get("symbols", []))
#                 socket_id = data.get("socket_id")
#                 socket_ids.append(socket_id)

#         # Create a dictionary to map socket IDs to symbols
#         socket_symbols_map = {socket_id: symbols for socket_id in socket_ids}

#         if access_token and symbols:
#             return access_token, symbols, socket_ids, socket_symbols_map

#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")

#     print(f"Failed to extract data from message: {message}")
#     print(f"Access Token: {access_token}")
#     print(f"Symbols: {symbols}")
#     print(f"Socket IDs: {socket_ids}")
#     print(f"Socket Symbols Map: {socket_symbols_map}")

#     return None, None, None, None


def extract_data_from_message(message):
    try:
        # Assuming message is a JSON-formatted data
        data_list = json.loads(message)

        # If data_list is not a list, convert it into a list
        if not isinstance(data_list, list):
            data_list = [data_list]

        access_token = None
        symbols = []
        socket_ids = []

        for data in data_list:
            if isinstance(data, dict) and "type" in data and data["type"] == "code_response":
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

    except ValueError as ve:
        print(f"ValueError: {ve}")

    print(f"Failed to extract data from message: {message}")
    print(f"Access Token: {access_token}")
    print(f"Symbols: {symbols}")
    print(f"Socket IDs: {socket_ids}")
    print(f"Socket Symbols Map: {socket_symbols_map}")

    return None, None, None, None





def subscribe_to_symbols(access_token, symbols):
    print("Subscribing to symbols")
    global subscribed_symbols  
    global fyers_instance  

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


app_8999 = Flask(__name__)
socketio_8999 = SocketIO(app_8999, cors_allowed_origins='*')

app_9999 = Flask(__name__)
socketio_9999 = SocketIO(app_9999, cors_allowed_origins='*')

# Define the event handler for Socket.IO connections
@socketio_8999.on('connect')
def handle_connect():
    sid = request.sid
    print(f"Client connected: {sid}")

# Define the event handler for Socket.IO disconnections
@socketio_8999.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

@socketio_8999.on('message')
def listen_to_external_websocket(data):
    global socket_symbols_map 
    global fyers_instance 

    try:
        print("Received data: ", data)
        # message = data['message']
        # print(f"Received message: {message}")

        # Extract access token, symbols, socket IDs, and socket-symbols map from the received message
        access_token, symbols, socket_ids, _ = extract_data_from_message(data)

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

            # Emit a message to the client that the data has been processed
            emit('external_message_processed', {'status': 'success'})

    except Exception as e:
        print(f"An error occurred: {e}")


# def run_server(app, socketio, port):
#     socketio.run(app, host='localhost', port=port)

# Start the Socket.IO server for listening
# if __name__ == '__main__':
#     socketio_8999.run(app_8999, port=8999)
#     socketio_9999.run(app_9999, port=9999)


if __name__ == '__main__':
    # Start the first Socket.IO server in a separate thread
    thread_8999 = Thread(target=socketio_8999.run, args=(app_8999, ), kwargs={'port': 8999})
    thread_8999.start()

    # Start the second Socket.IO server in the main thread
    socketio_9999.run(app_9999, port=9999)

# if __name__ == '__main__':
#     thread_8999 = Thread(target=socketio_8999.run, args=(app_8999, ), kwargs={'port': 8999})
#     thread_8999.start()
