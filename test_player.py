import asyncio
import websockets

async def receive_messages(websocket):
    """Continuously listens to messages from the server."""
    while True:
        try:
            response = await websocket.recv()
            print("\n💬 Server:", response)
            if "The game is starting!" in response:
                return  
            print("🛠️ Waiting for user input (or 'exit' to quit): ", end='', flush=True)
        except websockets.exceptions.ConnectionClosed:
            print("🔴 Connection closed by the server.")
            return

async def send_messages(websocket):
    """Sends player messages without blocking server message display."""
    while True:
        try:
            choice = await asyncio.to_thread(input)
            if choice.lower() == "exit":
                print("👋 Disconnecting...")
                await websocket.close()
                return
            await websocket.send(choice)
            print("✅ Message sent!")
            return
        except websockets.exceptions.ConnectionClosed:
            print("🔴 Connection closed by the server.")
            return

async def send_choice(websocket):
    """Handles sending the game choice."""
    try:
        choice = None
        while choice not in ["rock", "paper", "scissors", "fire", "water", "air", "sponge", "gun", "lightning", "devil"]:
            choice = await asyncio.to_thread(input, "Choose: rock, paper, scissor, fire, water, air, sponge, gun, lightning or devil: ")
            if choice not in ["rock", "paper", "scissors", "fire", "water", "air", "sponge", "gun", "lightning", "devil"]:
                print("❌ Invalid choice. Try again.")
        await websocket.send(choice)
        print("✅ Choice sent!")
        response = await websocket.recv()
        print("\n💬 Server:", response)
        response = await websocket.recv()
        print("\n💬 Server:", response)
        return response
    except websockets.exceptions.ConnectionClosed:
        print("🔴 Connection closed by the server.")
        return

async def connect_to_server():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("💬 Server: Connected to the WebSocket server")

        response = await websocket.recv()
        print("💬 Server:", response)

        choice = None
        while choice not in ["1", "2"]:
            choice = await asyncio.to_thread(input)
            if choice not in ["1", "2"]:
                print("❌ Invalid choice. Try again.")

        await websocket.send(choice)

        owner = choice == "1"

        if owner:
            response = await websocket.recv()
            name = await asyncio.to_thread(input, "💬 Server: " + response + " ")
            await websocket.send(name)
            response = await websocket.recv()
            print("💬 Server:", response)

        else:
            response = await websocket.recv()
            room_id = await asyncio.to_thread(input, "💬 Server: " + response + " ")
            await websocket.send(room_id)
            response = await websocket.recv()
            name = await asyncio.to_thread(input, "💬 Server: " + response + " ")
            await websocket.send(name)
            response = await websocket.recv()
            print("💬 Server:", response)

        if owner:
            # Launch listening and sending tasks in parallel for the owner
            receive_task = asyncio.create_task(receive_messages(websocket))
            send_task = asyncio.create_task(send_messages(websocket))  # To send messages continuously
            await asyncio.gather(receive_task, send_task)  # Wait for both tasks
        
        else:
            try:
                while True:
                    response = await websocket.recv()
                    print("\n💬 Server:", response)
                    if "The game is starting!" in response:
                        response = await send_choice(websocket)  # Send the choice as soon as The game is starting!
                        if "won" in response:
                            break
            except websockets.exceptions.ConnectionClosed:
                print("🔴 Connection closed by the server.")
                return
        # Wait for the owner to start the game
        if owner:
            try:
                while True:
                    response = await send_choice(websocket)  # Send the choice as soon as The game is starting!
                    if "won" in response:
                        break
            except websockets.exceptions.ConnectionClosed:
                print("🔴 Connection closed by the server.")
                return
# Launch the WebSocket client
asyncio.run(connect_to_server())
