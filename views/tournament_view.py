from models.tournament import Tournament, TournamentRepository
from models.player import PlayerRepository
import random
from datetime import datetime


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


def start_new_round_view():
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

    if tournament.current_round >= tournament.number_of_rounds:
        print("⚠️ Tous les rounds ont déjà été joués.")
        return

    if len(tournament.players) < 2:
        print("❌ Pas assez de joueurs inscrits pour générer un round.")
        return

    all_players = PlayerRepository.load_players()
    player_dict = {p.id: p for p in all_players}

    # Score par joueur
    scores = {pid: player_dict[pid].score for pid in tournament.players}

    # Tri des joueurs par score descendant
    sorted_players = sorted(tournament.players, key=lambda pid: (-scores[pid], random.random()))

    # Récupération des paires déjà jouées
    past_pairs = set()
    for round_ in tournament.rounds:
        for match in round_["matches"]:
            pair = tuple(sorted([match[0][0], match[1][0]]))
            past_pairs.add(pair)

    matches = []
    used = set()

    i = 0
    while i < len(sorted_players) - 1:
        pid1 = sorted_players[i]
        for j in range(i + 1, len(sorted_players)):
            pid2 = sorted_players[j]
            pair = tuple(sorted([pid1, pid2]))
            if pair not in past_pairs and pid1 not in used and pid2 not in used:
                matches.append([[pid1, 0.0], [pid2, 0.0]])
                used.add(pid1)
                used.add(pid2)
                break
        i += 1

    # Si joueur impair : il reste un joueur seul
    if len(used) < len(sorted_players):
        solo = [pid for pid in sorted_players if pid not in used][0]
        print(f"⚠️ Joueur seul ce round : {player_dict[solo].first_name} {player_dict[solo].last_name}")
        matches.append([[solo, 1.0], [None, 0.0]])  # Point gratuit

    round_number = tournament.current_round + 1
    round_name = f"Round {round_number}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_round = {
        "name": round_name,
        "start_time": now,
        "end_time": None,
        "matches": matches
    }

    tournament.rounds.append(new_round)
    tournament.current_round = round_number

    TournamentRepository.save_tournaments(tournaments)

    print(f"\n✅ {round_name} démarré avec {len(matches)} match(s).\n")


def enter_results_for_round_view():
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

    if not tournament.rounds:
        print("❌ Aucun round à gérer.")
        return

    # Dernier round non terminé
    current_round = None
    for r in tournament.rounds:
        if r["end_time"] is None:
            current_round = r
            break

    if not current_round:
        print("✅ Tous les rounds sont terminés.")
        return

    print(f"\n=== Saisie des résultats - {current_round['name']} ===")

    all_players = PlayerRepository.load_players()
    player_dict = {p.id: p for p in all_players}

    for idx, match in enumerate(current_round["matches"], start=1):
        player1_id, _ = match[0]
        player2_id, _ = match[1]

        if player2_id is None:
            print(f"Match {idx}: {player_dict[player1_id].first_name} {player_dict[player1_id].last_name}")
            match[0][1] = 1.0
            match[1][1] = 0.0
            continue

        p1 = player_dict[player1_id]
        p2 = player_dict[player2_id]

        print(f"\nMatch {idx}: {p1.first_name} {p1.last_name} VS {p2.first_name} {p2.last_name}")
        print("1. Victoire joueur 1")
        print("2. Victoire joueur 2")
        print("3. Match nul")

        while True:
            res = input("Résultat (1/2/3) : ").strip()
            if res == "1":
                match[0][1] = 1.0
                match[1][1] = 0.0
                break
            elif res == "2":
                match[0][1] = 0.0
                match[1][1] = 1.0
                break
            elif res == "3":
                match[0][1] = 0.5
                match[1][1] = 0.5
                break
            else:
                print("Entrée invalide. Réessayez.")

    # Mettre à jour les scores des joueurs
    for match in current_round["matches"]:
        for player_id, score in match:
            if player_id is not None:
                player_dict[player_id].score += score

    # Sauvegarder joueurs et tournoi
    PlayerRepository.save_players(list(player_dict.values()))
    current_round["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    TournamentRepository.save_tournaments(tournaments)

    print(f"\n✅ Résultats enregistrés pour {current_round['name']}.\n")


def show_rounds_history_view():
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

    if not tournament.rounds:
        print(f"\nAucun round enregistré pour « {tournament.name} ».\n")
        return

    all_players = PlayerRepository.load_players()
    player_dict = {p.id: f"{p.first_name} {p.last_name}" for p in all_players}

    print(f"\n=== Historique des rounds pour « {tournament.name} » ===")

    for rnd in tournament.rounds:
        print(f"\n➡️  {rnd['name']}")
        print(f"   Début : {rnd['start_time']}")
        print(f"   Fin   : {rnd['end_time'] or '⏳ En cours'}")
        print("   Matchs :")
        for idx, match in enumerate(rnd["matches"], start=1):
            p1_id, s1 = match[0]
            p2_id, s2 = match[1]
            p1_name = player_dict.get(p1_id, "??")
            p2_name = player_dict.get(p2_id, "Libre") if p2_id else "Libre"
            print(f"     {idx}. {p1_name} ({s1}) vs {p2_name} ({s2})")
    print()


def show_player_rankings_view():
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
        print("\nAucun joueur inscrit à ce tournoi.\n")
        return

    all_players = PlayerRepository.load_players()
    player_dict = {p.id: p for p in all_players}

    # Crée une liste [(joueur, score)] triée par score décroissant
    ranking = sorted(
        [(player_dict[pid], player_dict[pid].score) for pid in tournament.players],
        key=lambda x: -x[1]
    )

    print(f"\n=== Classement des joueurs – {tournament.name} ===")
    for rank, (player, score) in enumerate(ranking, start=1):
        print(f"{rank}. {player.first_name} {player.last_name} – {score} points")
    print()


def close_tournament_view():
    tournaments = TournamentRepository.load_tournaments()
    if not tournaments:
        print("\nAucun tournoi disponible.\n")
        return

    print("\n=== Clôturer un tournoi ===")
    for idx, t in enumerate(tournaments, start=1):
        status = "✅" if getattr(t, "is_closed", False) else "🕗"
        print(f"{idx}. {t.name} ({t.location}) {status}")

    try:
        choice = int(input("Choisissez le tournoi (numéro) : ")) - 1
        tournament = tournaments[choice]
    except (ValueError, IndexError):
        print("❌ Sélection invalide.")
        return

    if tournament.is_closed:
        print("\n❌ Ce tournoi est déjà clôturé.\n")
        return

    incomplete = [r for r in tournament.rounds if r["end_time"] is None]
    if incomplete:
        print("\n❌ Tous les rounds ne sont pas terminés. Impossible de clôturer.\n")
        return

    all_players = PlayerRepository.load_players()
    player_dict = {p.id: p for p in all_players}
    ranking = sorted(
        [(player_dict[pid], player_dict[pid].score) for pid in tournament.players],
        key=lambda x: -x[1]
    )

    print(f"\n=== Résumé final : {tournament.name} ===")
    print("📍 Lieu :", tournament.location)
    print("📅 Du", tournament.start_date, "au", tournament.end_date)
    print("\n🎖️ Classement final :")
    for rank, (player, score) in enumerate(ranking, start=1):
        print(f"{rank}. {player.first_name} {player.last_name} – {score} pts")

    print("\n📘 Rounds :")
    for rnd in tournament.rounds:
        print(f"- {rnd['name']} ({rnd['start_time']} → {rnd['end_time']})")

    confirm = input("\nConfirmer la clôture du tournoi ? (o/n) : ").strip().lower()
    if confirm == "o":
        tournament.is_closed = True
        TournamentRepository.save_tournaments(tournaments)
        print("\n✅ Tournoi clôturé avec succès.\n")
    else:
        print("\n❌ Clôture annulée.\n")
