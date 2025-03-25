from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import random
app = FastAPI(
    title="FastAPI WebSocket App",
    docs_url="/docs",
    description="A simple FastAPI app with WebSocket support and API documentation.",
    version="1.0.0"

)

# Sample user names
sample_users = {
    1: "Alice Smith",
    2: "Bob Johnson",
    3: "Charlie Brown",
    4: "David Wilson",
    5: "Eva Davis",
    6: "Frank Miller",
    7: "Grace Lee",
    8: "Hannah Clark",
    9: "Ivy Hall",
    10: "Jack Lewis",
    11: "Kara Young",
    12: "Liam Walker",
    13: "Mia King",
    14: "Noah Scott",
    15: "Olivia Adams",
    16: "Peter Carter",
    17: "Quinn Baker",
    18: "Rachel Evans",
    19: "Sam Harris",
    20: "Tina Moore",
    21: "Uma Thompson",
    22: "Victor Martinez",
    23: "Wendy Robinson",
    24: "Xander Mitchell",
    25: "Yara Perez",
    26: "Zane Jackson",
    27: "Amelia Hall",
    28: "Brayden King",
    29: "Clara Lopez",
    30: "Dylan Lewis"
}

# In-memory storage for chat rooms
class ChatRoom:
    def __init__(self, name: str):
        self.name = name
        self.clients: List[WebSocket] = []

    def add_client(self, client: WebSocket):
        self.clients.append(client)

    def remove_client(self, client: WebSocket):
        self.clients.remove(client)

    async def send_message(self, message: str, sender_name: str):
        formatted_message = f"{sender_name}: {message}"
        for client in self.clients:
            await client.send_text(formatted_message)

# In-memory rooms dictionary
rooms = {"Just Chat": ChatRoom(name="Just Chat")}

@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    # Check if the room exists
    if room_name not in rooms:
        await websocket.close()
        return
    
    room = rooms[room_name]
    await websocket.accept()
    room.add_client(websocket)

    # Assign a random user name from sample_users
    user_id = random.randint(1, len(sample_users))
    user_name = sample_users[user_id]

    # Send the assigned username to the client
    await websocket.send_text(f"Connected to the server with user name: {user_name}")
    
    try:
        while True:
            # Wait for message from the client
            message = await websocket.receive_text()
            # Send the message to all clients in the room with the user name
            await room.send_message(message, user_name)
    except WebSocketDisconnect:
        room.remove_client(websocket)
        print(f"🔴 {user_name} disconnected from {room_name}")
