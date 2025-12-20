import asyncio
import websockets
import json
import requests
import threading

# Function to safely post data without blocking the event loop
def post_data(data):
    try:
        print("Posting:", data)
        response = requests.post("http://localhost:8000/ingest", json=data, timeout=5)
        print("Status:", response.status_code)
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("POST failed:", e)

# Main async function to stream data from Coinbase WebSocket
async def stream_and_post():
    print("WebSocket task started")
    uri = "wss://ws-feed.exchange.coinbase.com"

    try:
        async with websockets.connect(uri) as websocket:
            subscribe_message = {
                "type": "subscribe",
                "channels": [{"name": "ticker", "product_ids": ["BTC-USD", "ETH-USD", "XRP-USD"]}]
            }
            await websocket.send(json.dumps(subscribe_message))
            print("Subscribed to Coinbase WebSocket")

            while True:
                try:
                    response = await websocket.recv()
                    data = json.loads(response)

                    if data.get("type") == "ticker":
                        threading.Thread(target=post_data, args=(data,)).start()
                except Exception as e:
                    print("Error in message loop:", e)
                    await asyncio.sleep(1)
    except Exception as e:
        print("WebSocket connection failed:", e)