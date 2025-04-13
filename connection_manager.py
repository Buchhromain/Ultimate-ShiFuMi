from fastapi import WebSocket
from typing import List
from player import Player
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_players: List[Player] = []

    async def connect(self, websocket: WebSocket, player_name: str) -> Player:
        """ Connecte un joueur et l'ajoute à la liste des joueurs actifs. """
        player = Player(websocket, player_name)  # 🔹 Inversion des arguments !
        print(f"👤 Nouveau joueur connecté : {player.name}, WebSocket: {player.websocket}")  # Debug
        self.active_players.append(player)
        return player

    def disconnect(self, player: Player):
        """ Déconnecte un joueur proprement. """
        if player in self.active_players:
            self.active_players.remove(player)
            print(f"🔴 {player.name} déconnecté.")

    async def send_to_all(self, message: str):
        """ Envoie un message à tous les joueurs connectés. """
        for player in self.active_players:
            await player.send_message(message)
    
    async def wait_for_opponent(self, player: Player):
        """ Attends qu'un autre joueur se connecte. """
        while len(self.active_players) < 2:  # Nous avons besoin de 2 joueurs pour commencer une partie
            await asyncio.sleep(0.1)  # Attendre sans bloquer le serveur

    async def get_opponent(self, player: Player) -> Player | None:
        """ Récupère l'adversaire d'un joueur. """
        for p in self.active_players:
            if p != player:
                return p
        return None  # Aucun adversaire trouvé
