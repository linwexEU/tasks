from fastapi import WebSocket


class ConnectionManager: 
    def __init__(self): 
        self.connections: list[WebSocket] = [] 

    async def connect(self, websocket: WebSocket): 
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket): 
        self.connections.remove(websocket) 

    async def send_message(self, message: dict): 
        for connections in self.connections: 
            await connections.send_json(message) 










