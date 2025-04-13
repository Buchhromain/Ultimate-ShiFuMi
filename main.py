from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager, Player
from room_manager import RoomManager  # Gestionnaire de rooms
from starlette.websockets import WebSocketState

app = FastAPI()
manager = ConnectionManager()
room_manager = RoomManager()


async def create_room(player: Player, websocket: WebSocket):
    """ Fonction pour créer une room """
    # Création d'une room
    await websocket.send_text("Enter your name: ")
    player_name = await websocket.receive_text()
    player = await manager.connect(websocket, player_name)

    room_id, room = room_manager.create_room(player)
    await player.send_message(f"Room created! Code: {room_id} - You are the host.")
    return room, player, room_id

async def join_room(player: Player, room_id: str, websocket: WebSocket):
    """ Fonction pour rejoindre une room """
    room = room_manager.get_room(room_id)

    if room is None:
        await websocket.send_text("Invalid room code.")
        return None

    await websocket.send_text("Enter your name: ")
    player_name = await websocket.receive_text()
    player = await manager.connect(websocket, player_name)

    if not room.add_player(player):
        await websocket.send_text("The game has already started. Connection closed.")
        return None

    await player.send_message(f"You have joined room {room_id}. Please wait for the host to start the game.")
    if room.owner:
        await room.owner.send_message(f"{player.name} has joined your room.")
    return room, player

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    player = None
    room = None

    try:
        # Demander au joueur s'il veut créer ou rejoindre une room
        await websocket.send_text("Do you want to (1) create a room or (2) join a room?")
        choice = await websocket.receive_text()

        if choice == "1":
            # Créer une nouvelle room
            room, player, room_id = await create_room(player, websocket)

        elif choice == "2":
            # Rejoindre une room existante
            await websocket.send_text("Enter the room code: ")
            room_id = await websocket.receive_text()
            room, player = await join_room(player, room_id, websocket)
            if room is None:
                await websocket.close()
                return
   
        else:
            await websocket.send_text("Invalid choice. Connection closed.")
            return

        # Attente du lancement du chef
        if player == room.owner:
            await player.send_message("Type 'start' to launch the game (or 'exit' to quit): ")
            start_command = await websocket.receive_text()
            if start_command.lower() == "start":
                room.game_started = True
                for p in room.players:
                    await p.send_message("The game is starting!")

        # Boucle principale : récupère les choix
        while not room.all_players_ready():
            try:
                choix = await websocket.receive_text()
                await player.set_choice(choix)
            except WebSocketDisconnect:
                print(f"❌ Déconnexion détectée pour {player.name}")
                room.remove_player(player)
                return

        # Annonce des choix
        await room.broadcast(f"{room.determine_winner()}")

    except WebSocketDisconnect:
        print(f"Déconnexion détectée pour {player.name if player else 'inconnu'}")
        if room:
            room.remove_player(player)
        if player:
            await manager.remove(player)

    except Exception as e:
        print(f"Erreur inattendue : {e}")

    finally:
        if player and player.websocket.client_state == WebSocketState.CONNECTED:
            try:
                print("Fermeture du WebSocket...")
                await player.websocket.close()
            except Exception as e:
                print(f"Erreur lors de la fermeture du WebSocket : {e}")