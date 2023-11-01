# import sys
# import json

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python main.py <token_symbol_map_json>")
#         sys.exit(1)

#     token_symbol_map_json = sys.argv[1]

#     # Parse the token_symbol_map from the JSON string
#     token_symbol_map = json.loads(token_symbol_map_json)

#     print("Received token_symbol_map in main.py:")
#     print(token_symbol_map)








import sys
import json
from multiprocessing import Process
from fyers_apiv3.FyersWebsocket import data_ws
from main import token_symbol_map


def onmessage(token_number, symbol, message):
    try:
        symbol_data = message
        print(f"Token {token_number} - Symbol {symbol} data: {symbol_data}")
        # Process and handle the data for the specific symbol here
    except KeyError as e:
        print("KeyError:", e)

def onerror(token_number, symbol, message):
    print(f"Token {token_number} - Symbol {symbol} Error:", message)

def onclose(token_number, symbol):
    print(f"Token {token_number} - Symbol {symbol} Connection closed")

def onopen(token_number, symbol):
    print(f"Token {token_number} - Symbol {symbol} WebSocket connection established")


def create_and_connect_socket(access_token, symbol):
    fyers_data = data_ws.FyersDataSocket(
        access_token=access_token,
        log_path="",
        litemode=False,
        write_to_file=False,
        reconnect=True,
        on_connect=lambda: onopen(access_token, symbol),
        on_close=lambda: onclose(access_token, symbol),
        on_error=lambda message: onerror(access_token, symbol, message),
        on_message=lambda message: onmessage(access_token, symbol, message)
    )
    fyers_data.connect()
    fyers_data.subscribe([symbol])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <token_symbol_map_json>")
        sys.exit(1)

    token_symbol_map_json = sys.argv[1]

    # Parse the token_symbol_map from the JSON string
    token_symbol_map = json.loads(token_symbol_map_json)

    print("Received token_symbol_map in main.py:")
    print(token_symbol_map)

    # Now you can use token_symbol_map in your main.py as needed

    processes = []
    for access_token, symbols in token_symbol_map.items():
        for symbol in symbols:
            process = Process(target=create_and_connect_socket, args=(access_token, symbol))
            processes.append(process)
            process.start()

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()



