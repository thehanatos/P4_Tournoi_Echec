import json
import os
from datetime import datetime

DATA_FILE = "/home/watashi/Projets/P5_Tournoi_Echec/data/players.json"


class Player:
    def __init__(self, last_name, first_name, birth_date, player_id=None):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date  # format: YYYY-MM-DD
        self.id = player_id or f"{first_name.lower()}_{last_name.lower()}_{birth_date}"
        self.score = 0

    def to_dict(self):
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "score": self.score
        }

    @staticmethod
    def from_dict(data):
        player = Player(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birth_date=data["birth_date"],
            player_id=data["id"]
        )
        player.score = data.get("score", 0)
        return player


class PlayerRepository:
    @staticmethod
    def load_players():
        if not os.path.exists(DATA_FILE):
            return []

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [Player.from_dict(p) for p in data]

    @staticmethod
    def save_players(players):
        with open(DATA_FILE, "w") as f:
            json.dump([p.to_dict() for p in players], f, indent=4)

    @staticmethod
    def add_player(player):
        players = PlayerRepository.load_players()
        players.append(player)
        PlayerRepository.save_players(players)
