from models.player import Player, PlayerRepository


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

    PlayerRepository.add_player(player)
    print(f"\n✅ Player {first_name} {last_name} enregistré avec succès.\n")
