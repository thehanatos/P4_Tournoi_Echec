from models.player import PlayerRepository
from controllers.player_controller import PlayerController
import re
from datetime import datetime


def validate_name(name):
    """
    Validates that a name contains only letters, hyphens, or spaces and is at least two characters long.
    """
    return bool(re.fullmatch(r"[A-Za-zÀ-ÿ\- ]{2,}", name))


def validate_birth_date(date_str):
    """
    Validates that the date is in the format YYYY-MM-DD and is not a future date.
    """
    try:
        birth_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return birth_date <= datetime.today().date()
    except ValueError:
        return False


def create_player_view():
    """
    Handles user input for creating a new player.
    """
    print("=== Création d'un nouveau joueur ===")

    while True:
        first_name = input("Prénom : ").strip()
        if validate_name(first_name):
            break
        print("❌ Le prénom est invalide. Utilisez uniquement des lettres (minimum 2).")

    while True:
        last_name = input("Nom de famille : ").strip()
        if validate_name(last_name):
            break
        print("❌ Le nom est invalide. Utilisez uniquement des lettres (minimum 2).")

    while True:
        birth_date = input("Date de naissance (YYYY-MM-DD) : ").strip()
        if validate_birth_date(birth_date):
            break
        print("❌ Format ou date invalide. Utilisez le format YYYY-MM-DD et une date passée.")

    player = PlayerController.create_player(first_name, last_name, birth_date)
    print(f"\n✅ Player {player.first_name} {player.last_name} enregistré avec succès.\n")


def list_players_view():
    """
    Displays a sorted list of all registered players.
    Players are sorted by last name and then first name.
    Includes their birth date and current score.
    """
    players = PlayerRepository.load_players()

    if not players:
        print("\nAucun joueur enregistré.\n")
        return

    print("\n=== Liste des joueurs enregistrés ===")
    players.sort(key=lambda p: (p.last_name.lower(), p.first_name.lower()))

    for idx, player in enumerate(players, start=1):
        print(f"{idx}. {player.first_name} {player.last_name} - Né(e) le {player.birth_date} - Score: {player.score}")
    print()
