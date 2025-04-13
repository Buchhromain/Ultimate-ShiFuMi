import random
import string
from player import Player

class Room:
    def __init__(self, room_id, owner: Player):
        self.room_id = room_id  # Code unique de la room
        self.owner = owner  # Le joueur qui a créé la room (chef)
        self.players = [owner]  # Liste des joueurs
        self.game_started = False  # Indique si la partie est en cours
        self.choices = {}  # Stocke les choix des joueurs
        self.winning_cases = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }

    def add_player(self, player: Player):
        if self.game_started:
            return False  # On ne peut pas rejoindre une partie en cours
        self.players.append(player)
        return True

    def remove_player(self, player: Player):
        """Retire un joueur de la room."""
        if player in self.players:
            self.players.remove(player)
            print(f"🔴 {player.name} a quitté la room.")
            return True
        return False

    def all_players_ready(self):
        """Vérifie si tous les joueurs ont fait leur choix."""
        for player in self.players:
            if player.get_choice() is None:
                return False
        return True

    def determine_winner(self):
        """Détermine le gagnant (logique simplifiée pour l'instant)."""
        if self.players[0].get_choice() == self.players[1].get_choice():
            return "Match nul!"
        
        print(f"Choix des joueurs : {self.winning_cases[self.players[0].get_choice()]}")  # Debug
        print(f"Choix des joueurs : {self.winning_cases[self.players[1].get_choice()]}")  # Debug
        if self.winning_cases[self.players[0].get_choice()] == self.players[1].get_choice():
            return f"{self.players[0].name} won!"
        else:
            return f"{self.players[1].name} won!"
        
    async def broadcast(self, message: str):
        """Envoie un message à tous les joueurs de la room."""
        for player in self.players:
            await player.send_message(message)
        

class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self, owner):
        """Crée une nouvelle room avec un ID unique."""
        room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  # Ex: "A1B2C3"
        room = Room(room_id, owner)
        self.rooms[room_id] = room
        return room_id, room

    def get_room(self, room_id):
        return self.rooms.get(room_id, None)

    def remove_room(self, room_id):
        """Supprime une room si elle est vide."""
        if room_id in self.rooms:
            del self.rooms[room_id]
