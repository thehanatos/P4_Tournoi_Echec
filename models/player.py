import json
import os

DATA_FILE = "data/players.json"


class Player:
    """
    Represents a chess tournament player.
    """
    def __init__(self, last_name, first_name, birth_date, player_id=None):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date  # format: YYYY-MM-DD
        self.id = player_id or f"{first_name.lower()}_{last_name.lower()}_{birth_date}"
        self.score = 0

    def to_dict(self):
        """
        Convert the Player object to a dictionary format for serialization.
        """
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "score": self.score
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Player object from a dictionary.
        """
        player = Player(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birth_date=data["birth_date"],
            player_id=data["id"]
        )
        player.score = data.get("score", 0)
        return player


class PlayerRepository:
    """
    Repository class for handling persistence of Player data.
    """
    @staticmethod
    def load_players():
        """
        Load all players from the JSON data file.
        """
        if not os.path.exists(DATA_FILE):
            return []

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [Player.from_dict(p) for p in data]

    @staticmethod
    def save_players(players):
        """
        Save a list of players to the JSON data file.
        """
        with open(DATA_FILE, "w") as f:
            json.dump([p.to_dict() for p in players], f, indent=4)

    @staticmethod
    def add_player(player):
        """
        Add a new player to the repository and save the updated list.
        """
        players = PlayerRepository.load_players()
        players.append(player)
        PlayerRepository.save_players(players)
