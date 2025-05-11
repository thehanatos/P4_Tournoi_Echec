from models.tournament import Tournament, TournamentRepository


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
