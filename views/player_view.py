from models.player import Player, PlayerRepository
from controllers.player_controller import PlayerController


def create_player_view():
    print("=== Création d'un nouveau joueur ===")
    first_name = input("Prénom : ").strip()
    last_name = input("Nom de famille : ").strip()
    birth_date = input("Date de naissance (YYYY-MM-DD) : ").strip()

    player = Player(
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date
    )

    player = PlayerController.create_player(first_name, last_name, birth_date)
    print(f"\n✅ Player {player.first_name} {player.last_name} enregistré avec succès.\n")


def list_players_view():
    players = PlayerRepository.load_players()

    if not players:
        print("\nAucun joueur enregistré.\n")
        return

    print("\n=== Liste des joueurs enregistrés ===")
    players.sort(key=lambda p: (p.last_name.lower(), p.first_name.lower()))

    for idx, player in enumerate(players, start=1):
        print(f"{idx}. {player.first_name} {player.last_name} - Né(e) le {player.birth_date} - Score: {player.score}")
    print()
