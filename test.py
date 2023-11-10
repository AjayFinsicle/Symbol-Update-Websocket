import asyncio
import websockets
import json
import subprocess
import sys
from multiprocessing import Process
from fyers_apiv3.FyersWebsocket import data_ws
import time 

token_symbol_map = {}

# Reicieving the response from external websocket
async def handle_websocket_connection(websocket, path):
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            data_list = json.loads(message)

            for data_dict in data_list:
                if data_dict.get("type") == "code_response":
                    access_token = data_dict.get("token")
                    symbols = data_dict.get("symbols")

                    # Update the access token and symbols in the dictionary
                    token_symbol_map[access_token] = symbols

            print("--------------------------------------------------")
            print("Token Symbols map", token_symbol_map)

            

            # Start the WebSocket connection for received tokens and symbols
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

    except websockets.exceptions.ConnectionClosedError:
        pass


# Creating fyers instance using the response obtained from the external websocket connection
def create_and_connect_socket(access_token, symbol):
        print(access_token)
        print(symbol)
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
        print("Connected")


def onmessage(token_number, symbol, message):
    while True:
        try:
            symbol_data = message
            if symbol_data is None:
                print("Heart beat")
            print(f"Token {token_number} - Symbol {symbol} data: {symbol_data}")
            time.sleep(10)

        except KeyError as e:
            print("KeyError:", e)
    

def onerror(token_number, symbol, message):
    print(f"Token {token_number} - Symbol {symbol} Error:", message)

def onclose(token_number, symbol):
    print(f"Token {token_number} - Symbol {symbol} Connection closed")

def onopen(token_number, symbol):
    print(f"Token {token_number} - Symbol {symbol} WebSocket connection established")


if __name__ == "__main__":
    start_server = websockets.serve(handle_websocket_connection, "localhost", 8999)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
