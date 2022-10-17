import websocket


def on_message(data):
    pass


def on_open(data):
    print('Opened connection!')


ws = websocket.WebSocketApp(
    'ws://127.0.0.1:8000/chat/',
    on_open=on_open,
    on_message=on_message,
)
ws.run_forever()
