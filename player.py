from fastapi import WebSocket
from starlette.websockets import WebSocketState
import asyncio  # <-- Ajout de asyncio pour le verrou

class Player:
    def __init__(self, websocket: WebSocket, name: str):
        self.websocket = websocket
        self.name = name
        self.choice = None
        self.lock = asyncio.Lock()  # 🔹 Ajout d'un verrou

    async def set_choice(self, choice: str):
        """ Définit le choix du joueur """
        async with self.lock:
            self.choice = choice
        await self.send_message(f"Votre choix : {self.choice}")
        print(f"✅ {self.name} a choisi {self.choice}")

    def get_choice(self):
        return self.choice
    
    async def close(self):
        """ Ferme la connexion WebSocket """
        if self.websocket.client_state == WebSocketState.CONNECTED:
            await self.websocket.close()
            print(f"🔴 {self.name} déconnecté.")
        else:
            print(f"⚠️ {self.name} : WebSocket déjà fermé.")

    async def send_message(self, message: str):
        try:
            if self.websocket.client_state != WebSocketState.CONNECTED:
                print(f"⚠️ Tentative d'envoi à {self.name}, mais WebSocket fermé !")
                return
            await self.websocket.send_text(message)
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi d'un message à {self.name} : {e}")

    async def receive_choice(self):
        """ Reçoit le choix du joueur en utilisant un verrou pour éviter les conflits """
        async with self.lock:  # 🔹 Empêche plusieurs appels en concurrence
            try:
                if self.websocket.client_state == WebSocketState.CONNECTED:
                    self.choice = await self.websocket.receive_text()
                    print(f"✅ {self.name} a choisi {self.choice}")
            except Exception as e:
                print(f"🚨 Erreur de réception du choix de {self.name} : {e}")