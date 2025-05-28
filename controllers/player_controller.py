from models.player import Player, PlayerRepository


class PlayerController:

    @staticmethod
    def create_player(first_name, last_name, birth_date):
        """
        Create a new player and save it to the repository.
        """
        player = Player(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date
        )
        PlayerRepository.add_player(player)
        return player

    @staticmethod
    def get_all_players(sorted_by_name=True):
        """
        Retrieve all players from the repository.
        """
        players = PlayerRepository.load_players()
        if sorted_by_name:
            players.sort(key=lambda p: (p.last_name.lower(), p.first_name.lower()))
        return players
