from controllers.tournament_controller import TournamentController
from models.player import PlayerRepository
import re
from datetime import datetime


def validate_text_field(text):
    """
    Validates a general text field (name, location, etc.).
    """
    return bool(re.fullmatch(r"[A-Za-z0-9À-ÿ ,.'\-]{2,}", text))


def validate_date(date_str):
    """
    Validates and parses a date string in the format YYYY-MM-DD.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def create_tournament_view():
    """
    Interactive CLI view for creating a new tournament.

    Prompts the user for tournament details (name, location, start/end dates, description),
    validates inputs, and passes the data to the TournamentController for creation.
    """
    print("\n=== Création d’un nouveau tournoi ===")

    while True:
        name = input("Nom du tournoi : ").strip()
        if validate_text_field(name):
            break
        print("❌ Nom invalide. Minimum 2 caractères, lettres/chiffres/espaces autorisés.")

    while True:
        location = input("Lieu : ").strip()
        if validate_text_field(location):
            break
        print("❌ Lieu invalide. Minimum 2 caractères, lettres/chiffres/espaces autorisés.")

    while True:
        start_date_str = input("Date de début (YYYY-MM-DD) : ").strip()
        start_date = validate_date(start_date_str)
        if start_date and start_date >= datetime.today().date():
            break
        print("❌ Date de début invalide ou passée.")

    while True:
        end_date_str = input("Date de fin (YYYY-MM-DD) : ").strip()
        end_date = validate_date(end_date_str)
        if end_date and end_date >= start_date:
            break
        print("❌ Date de fin invalide ou antérieure à la date de début.")

    description = input("Description (facultatif) : ").strip()

    TournamentController.create_tournament(
        name=name,
        location=location,
        start_date=start_date_str,
        end_date=end_date_str,
        description=description
    )

    print(f"\n✅ Tournoi « {name} » enregistré avec succès.\n")


def list_tournaments_view():
    """
    Displays a list of all saved tournaments with basic details like name, location,
    dates, round progress, and number of registered players.
    """
    tournaments = TournamentController.get_all_tournaments()

    if not tournaments:
        print("\nAucun tournoi enregistré.\n")
        return

    print("\n=== Liste des tournois ===")
    for idx, t in enumerate(tournaments, start=1):
        print(f"{idx}. {t.name} ({t.location}) - {t.start_date} → {t.end_date}")
        print(f"   Description : {t.description}")
        print(f"   Rounds : {t.current_round}/{t.number_of_rounds} | Joueurs inscrits : {len(t.players)}\n")


def register_players_to_tournament_view():
    """
    Allows the user to select a tournament and register one or more players from the available list.
    """
    tournaments = TournamentController.get_all_tournaments()
    if not tournaments:
        print("\nAucun tournoi disponible.\n")
        return

    print("\n=== Sélection du tournoi ===")
    for idx, t in enumerate(tournaments, start=1):
        print(f"{idx}. {t.name} ({t.location})")

    try:
        tournament_index = int(input("Choisissez le tournoi (numéro) : ")) - 1
        tournament = tournaments[tournament_index]
    except (ValueError, IndexError):
        print("❌ Sélection invalide.")
        return

    players = PlayerRepository.load_players()
    if not players:
        print("\nAucun joueur disponible à inscrire.\n")
        return

    print("\n=== Joueurs disponibles ===")
    player_dict = {}
    for idx, p in enumerate(players, start=1):
        if p.id not in tournament.players:
            print(f"{idx}. {p.first_name} {p.last_name} ({p.birth_date})")
            player_dict[idx] = p

    selected = input("Entrez les numéros des joueurs à inscrire (ex: 1 3 5) : ").strip().split()
    selected_ids = []
    for sid in selected:
        try:
            selected_ids.append(player_dict[int(sid)].id)
        except (ValueError, KeyError):
            print(f"⚠️ Numéro invalide ou déjà inscrit : {sid}")

    added_count = TournamentController.register_players_to_tournament(tournament, selected_ids)
    print(f"\n✅ {added_count} joueur(s) inscrit(s) dans le tournoi « {tournament.name} ».\n")


def show_players_in_tournament_view():
    """
    Displays all players currently registered in a selected tournament,
    along with their name, birth date, and current score.
    """
    tournament = _select_tournament()
    if not tournament:
        return

    if not tournament.players:
        print(f"\nAucun joueur inscrit dans le tournoi « {tournament.name} ».\n")
        return

    registered_players = TournamentController.get_players_in_tournament(tournament)
    print(f"\n=== Joueurs inscrits dans « {tournament.name} » ===")
    for idx, p in enumerate(registered_players, start=1):
        print(f"{idx}. {p.first_name} {p.last_name} ({p.birth_date}) - Score: {p.score}")
    print()


def start_new_round_view():
    """
    Starts a new round in the selected tournament using the TournamentController.
    """
    tournament = _select_tournament()
    if not tournament:
        return

    result, message = TournamentController.start_new_round(tournament)
    if message:
        print(f"\n❌ {message}\n")
    elif result:
        print(f"\n✅ Nouveau round démarré : {result['name']}\n")
    else:
        print("\n❌ Erreur inconnue lors du démarrage du round.\n")


def enter_results_for_round_view():
    """
    Allows the user to input match results for the current round of a selected tournament.

    Supports 3 outcomes: player 1 wins, player 2 wins, or draw.
    """
    tournament = _select_tournament()
    if not tournament:
        return

    current_round = TournamentController.get_current_round(tournament)
    if not current_round:
        print("✅ Tous les rounds sont terminés.")
        return

    print(f"\n=== Saisie des résultats - {current_round['name']} ===")
    player_dict = {p.id: p for p in PlayerRepository.load_players()}

    for idx, match in enumerate(current_round["matches"], start=1):
        p1_id, _ = match[0]
        p2_id, _ = match[1]

        if p2_id is None:
            print(
                f"Match {idx}: {player_dict[p1_id].first_name} {player_dict[p1_id].last_name} reçoit 1 point.")
            TournamentController.set_match_result(match, 1.0, 0.0)
            continue

        p1 = player_dict[p1_id]
        p2 = player_dict[p2_id]

        print(f"\nMatch {idx}: {p1.first_name} {p1.last_name} VS {p2.first_name} {p2.last_name}")
        print("1. Victoire joueur 1")
        print("2. Victoire joueur 2")
        print("3. Match nul")

        while True:
            res = input("Résultat (1/2/3) : ").strip()
            if res == "1":
                TournamentController.set_match_result(match, 1.0, 0.0)
                break
            elif res == "2":
                TournamentController.set_match_result(match, 0.0, 1.0)
                break
            elif res == "3":
                TournamentController.set_match_result(match, 0.5, 0.5)
                break
            else:
                print("Entrée invalide. Réessayez.")

    TournamentController.finalize_round(tournament)
    print(f"\n✅ Résultats enregistrés pour {current_round['name']}.\n")


def show_rounds_history_view():
    """
    Displays a detailed history of all completed rounds in a selected tournament.
    """
    tournament = _select_tournament()
    if not tournament:
        return

    rounds = tournament.rounds
    player_names = {p.id: f"{p.first_name} {p.last_name}" for p in PlayerRepository.load_players()}

    if not rounds:
        print(f"\nAucun round enregistré pour « {tournament.name} ».\n")
        return

    print(f"\n=== Historique des rounds pour « {tournament.name} » ===")
    for rnd in rounds:
        print(f"\n➡️  {rnd['name']}")
        print(f"   Début : {rnd['start_time']}")
        print(f"   Fin   : {rnd['end_time'] if rnd['end_time'] else '⏳ En cours'}")
        print("   Matchs :")
        for idx, match in enumerate(rnd["matches"], start=1):
            p1_id, s1 = match[0]
            p2_id, s2 = match[1]
            p1_name = player_names.get(p1_id, "??")
            p2_name = player_names.get(p2_id, "Libre") if p2_id else "Libre"
            print(f"     {idx}. {p1_name} ({s1}) vs {p2_name} ({s2})")
    print()


def show_player_rankings_view():
    """
    Displays the current player rankings for a selected tournament.
    """
    tournament = _select_tournament()
    if not tournament:
        return

    ranking = TournamentController.get_tournament_rankings(tournament)

    print(f"\n=== Classement des joueurs – {tournament.name} ===")
    for rank, (player, score) in enumerate(ranking, start=1):
        print(f"{rank}. {player.first_name} {player.last_name} – {score} points")
    print()


def close_tournament_view():
    """
    Handles closing a tournament after verifying that all rounds are complete.
    """
    tournament = _select_tournament()
    if not tournament:
        return

    if tournament.is_closed:
        print("\n❌ Ce tournoi est déjà clôturé.\n")
        return

    if TournamentController.has_incomplete_rounds(tournament):
        print("\n❌ Tous les rounds ne sont pas terminés. Impossible de clôturer.\n")
        return

    TournamentController.display_final_summary(tournament)

    confirm = input("\nConfirmer la clôture du tournoi ? (o/n) : ").strip().lower()
    if confirm == "o":
        TournamentController.close_tournament(tournament)
        print("\n✅ Tournoi clôturé avec succès.\n")
    else:
        print("\n❌ Clôture annulée.\n")


def _select_tournament():
    """
    Displays a list of available tournaments and prompts the user to select one.
    """
    tournaments = TournamentController.get_all_tournaments()
    if not tournaments:
        print("\nAucun tournoi disponible.\n")
        return None

    print("\n=== Sélection du tournoi ===")
    for idx, t in enumerate(tournaments, start=1):
        print(f"{idx}. {t.name} ({t.location})")

    try:
        return tournaments[int(input("Choisissez le tournoi (numéro) : ")) - 1]
    except (ValueError, IndexError):
        print("❌ Sélection invalide.")
        return None
