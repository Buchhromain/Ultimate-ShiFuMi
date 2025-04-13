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
        self.winning_cases = {}
        self.elements = [
            "rock", "paper", "scissors", "fire", "water", "air", "sponge", "gun", "lightning", "devil"
        ]
        for i, elem in enumerate(self.elements):
            beats = [self.elements[(i + j) % len(self.elements)] for j in range(1, 6)]
            self.winning_cases[elem] = beats

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
        """Détermine le ou les gagnants parmi plusieurs joueurs dans l'Ultimate Shifumi."""
        scores = {player.name: 0 for player in self.players}
        choices = {player.name: player.get_choice() for player in self.players}

        # Tous les choix faits
        unique_choices = set(choices.values())
        if len(unique_choices) == 1:
            return "Match nul ! Tous les joueurs ont choisi la même chose."

        # Comparer tous les joueurs entre eux
        for i, player1 in enumerate(self.players):
            choice1 = player1.get_choice()
            for j, player2 in enumerate(self.players):
                if i == j:
                    continue
                choice2 = player2.get_choice()
                if choice2 in self.winning_cases[choice1]:
                    scores[player1.name] += 1

        # Trouver le score max
        max_score = max(scores.values())
        winners = [name for name, score in scores.items() if score == max_score]

        if len(winners) == 1:
            return f"{winners[0]} has won the round !"
        else:
            return f"deuce between : {', '.join(winners)}"
        
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
