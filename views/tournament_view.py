from models.tournament import Tournament, TournamentRepository
from models.player import PlayerRepository


def create_tournament_view():
    print("\n=== Création d’un nouveau tournoi ===")
    name = input("Nom du tournoi : ").strip()
    location = input("Lieu : ").strip()
    start_date = input("Date de début (YYYY-MM-DD) : ").strip()
    end_date = input("Date de fin (YYYY-MM-DD) : ").strip()
    description = input("Description : ").strip()

    tournament = Tournament(
        name=name,
        location=location,
        start_date=start_date,
        end_date=end_date,
        description=description
    )

    TournamentRepository.add_tournament(tournament)
    print(f"\n✅ Tournoi « {name} » enregistré avec succès.\n")


def list_tournaments_view():
    tournaments = TournamentRepository.load_tournaments()

    if not tournaments:
        print("\nAucun tournoi enregistré.\n")
        return

    print("\n=== Liste des tournois ===")
    for idx, t in enumerate(tournaments, start=1):
        print(f"{idx}. {t.name} ({t.location}) - {t.start_date} → {t.end_date}")
        print(f"   Description : {t.description}")
        print(f"   Rounds : {t.current_round}/{t.number_of_rounds} | Joueurs inscrits : {len(t.players)}\n")


def register_players_to_tournament_view():
    tournaments = TournamentRepository.load_tournaments()
    if not tournaments:
        print("\nAucun tournoi disponible.\n")
        return

    print("\n=== Sélection du tournoi ===")
    for idx, t in enumerate(tournaments, start=1):
        print(f"{idx}. {t.name} ({t.location})")

    try:
        choice = int(input("Choisissez le tournoi (numéro) : ")) - 1
        tournament = tournaments[choice]
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

    selected_ids = input("Entrez les numéros des joueurs à inscrire (ex: 1 3 5) : ").strip().split()

    added_count = 0
    for sid in selected_ids:
        try:
            player = player_dict[int(sid)]
            if player.id not in tournament.players:
                tournament.players.append(player.id)
                added_count += 1
        except (ValueError, KeyError):
            print(f"⚠️ Numéro invalide ou déjà inscrit : {sid}")

    TournamentRepository.save_tournaments(tournaments)

    print(f"\n✅ {added_count} joueur(s) inscrit(s) dans le tournoi « {tournament.name} ».\n")


def show_players_in_tournament_view():
    tournaments = TournamentRepository.load_tournaments()
    if not tournaments:
        print("\nAucun tournoi disponible.\n")
        return

    print("\n=== Sélection du tournoi ===")
    for idx, t in enumerate(tournaments, start=1):
        print(f"{idx}. {t.name} ({t.location})")

    try:
        choice = int(input("Choisissez le tournoi (numéro) : ")) - 1
        tournament = tournaments[choice]
    except (ValueError, IndexError):
        print("❌ Sélection invalide.")
        return

    if not tournament.players:
        print(f"\nAucun joueur inscrit dans le tournoi « {tournament.name} ».\n")
        return

    all_players = PlayerRepository.load_players()
    registered_players = [p for p in all_players if p.id in tournament.players]

    print(f"\n=== Joueurs inscrits dans « {tournament.name} » ===")
    for idx, p in enumerate(registered_players, start=1):
        print(f"{idx}. {p.first_name} {p.last_name} ({p.birth_date}) - Score: {p.score}")
    print()
