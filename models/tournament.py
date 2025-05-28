import json
import os
import uuid

TOURNAMENTS_FILE = "data/tournaments.json"


class Tournament:
    """
    Represents a chess tournament with relevant attributes such as name, location, date, players, and rounds.
    """
    def __init__(
            self, name, location, start_date, end_date, description, id=None, number_of_rounds=4, is_closed=False):
        """
        Initializes a new Tournament instance.
        """
        self.name = name
        self.location = location
        self.start_date = start_date  # format: YYYY-MM-DD
        self.end_date = end_date      # format: YYYY-MM-DD
        self.description = description
        self.id = id or str(uuid.uuid4())
        self.number_of_rounds = number_of_rounds
        self.current_round = 0
        self.rounds = []        # List of rounds
        self.players = []       # List of player IDs
        self.is_closed = is_closed

    def to_dict(self):
        """
        Converts the Tournament object into a dictionary format for serialization.
        """
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "id": self.id,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": self.rounds,
            "players": self.players,
            "is_closed": self.is_closed
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Tournament object from a dictionary.
        """
        tournament = Tournament(
            id=data.get("id"),
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data["description"],
            number_of_rounds=data.get("number_of_rounds", 4),
            is_closed=data.get("is_closed", False)
        )
        tournament.current_round = data.get("current_round", 0)
        tournament.rounds = data.get("rounds", [])
        tournament.players = data.get("players", [])
        return tournament


class TournamentRepository:
    """
    Handles loading, saving, and updating tournament data to and from the JSON file.
    """
    @staticmethod
    def load_tournaments():
        """
        Loads all tournaments from the JSON file.
        """
        if not os.path.exists(TOURNAMENTS_FILE):
            return []
        with open(TOURNAMENTS_FILE, "r") as f:
            data = json.load(f)
            return [Tournament.from_dict(t) for t in data]

    @staticmethod
    def save_tournaments(tournaments):
        """
        Saves the given list of tournaments to the JSON file.
        """
        with open(TOURNAMENTS_FILE, "w") as f:
            json.dump([t.to_dict() for t in tournaments], f, indent=4)

    @staticmethod
    def add_tournament(tournament):
        """
        Adds a new tournament to the list and saves it.
        """
        tournaments = TournamentRepository.load_tournaments()
        tournaments.append(tournament)
        TournamentRepository.save_tournaments(tournaments)
