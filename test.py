from multiprocessing import Process
from fyers_apiv3.FyersWebsocket import data_ws
import asyncio
import websockets
import json



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

client_id = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"

if __name__ == "__main__":
    token_symbol_map = {
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTg4MjY1OTUsImV4cCI6MTY5ODg4NTAzNSwibmJmIjoxNjk4ODI2NTk1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbFFnbGpaOThsd1hWNTl2SUdRR0VRUkp1YmNCUHNoSUFUaTJxVmxfU1pJekZsNmFYNHVmYkI1MEh6S0huLWNuQXFSS2pBN1ZUWGxIa3ZtOV9pOWU4WDU1bWZPTjdJeE9XdS14UmotbFI3Um1Rd2hobz0iLCJkaXNwbGF5X25hbWUiOiJGSU5TSUNMRSBQUklWQVRFIExJTUlURUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI4OGE2NzUwYjc4ZmNiNWI2NGZhOWVlZTQ2NTlkZTVkZDFhY2M0MWFmNzJiOWZlNWU1MDBhYTg0NyIsImZ5X2lkIjoiQ0EwMDEzOCIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.e-MmGMm6JZbUYOCQ-Cn60itspxt_q4zAMQgDsw0jCVQ": ["NSE:NIFTY50-INDEX"],
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTg4MjY2MjgsImV4cCI6MTY5ODg4NTAwOCwibmJmIjoxNjk4ODI2NjI4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbFFnbUVMSXd1XzBwbUxJRDVHTHZjSjFWV1ljQlF0SUJzNEpwOUFTbWdSSk5BVXlUWVJ4RmdQMm02WEFLVHNncWE0cHN0TkowdFZqNFh4Q1dfZURRdlZzVFVrV1FRakNNZFJkUGlpTFpIdUdrV1FVMD0iLCJkaXNwbGF5X25hbWUiOiJGSU5TSUNMRSBQUklWQVRFIExJTUlURUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI4OGE2NzUwYjc4ZmNiNWI2NGZhOWVlZTQ2NTlkZTVkZDFhY2M0MWFmNzJiOWZlNWU1MDBhYTg0NyIsImZ5X2lkIjoiQ0EwMDEzOCIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.-78lZgb4tNXqmREdakggdmA2af8XPBYL-KoWgiKqihQ": ["NSE:FINNIFTY-INDEX"]
    }

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
