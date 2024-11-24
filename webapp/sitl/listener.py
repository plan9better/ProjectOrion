import websockets
async def listen_for_messages():
    uri = "ws://localhost:8765"  # Address of the WebSocket server
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()  # Wait to receive a message
                return message
        except websockets.ConnectionClosed:
            pass