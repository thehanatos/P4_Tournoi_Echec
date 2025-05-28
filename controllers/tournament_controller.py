from models.tournament import Tournament, TournamentRepository
from models.player import PlayerRepository
from datetime import datetime
import random


class TournamentController:
    @staticmethod
    def create_tournament(name, location, start_date, end_date, description):
        """
        Create a new tournament and save it to the repository.
        """
        tournament = Tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        TournamentRepository.add_tournament(tournament)
        return tournament

    @staticmethod
    def get_all_tournaments():
        """
        Load and return all tournaments from the repository.
        """
        return TournamentRepository.load_tournaments()

    @staticmethod
    def get_all_players():
        """
        Load and return all registered players.
        """
        return PlayerRepository.load_players()

    @staticmethod
    def register_players_to_tournament(tournament, player_ids):
        """
        Register multiple players to a given tournament.
        """
        added = 0
        for pid in player_ids:
            if pid not in tournament.players:
                tournament.players.append(pid)
                added += 1

        all_tournaments = TournamentController.get_all_tournaments()
        for i, t in enumerate(all_tournaments):
            if t.id == tournament.id:
                all_tournaments[i] = tournament
                break

        TournamentRepository.save_tournaments(all_tournaments)
        return added

    @staticmethod
    def get_players_in_tournament(tournament):
        """
        Retrieve player objects registered in a given tournament.
        """
        all_players = TournamentController.get_all_players()
        return [p for p in all_players if p.id in tournament.players]

    @staticmethod
    def start_new_round(tournament):
        """
        Start a new round in the tournament, generate matches,
        and update the tournament accordingly.
        """
        if tournament.current_round >= tournament.number_of_rounds:
            return None, "Tous les rounds ont déjà été joués."

        if len(tournament.players) < 2:
            return None, "Pas assez de joueurs inscrits pour générer un round."

        all_players = TournamentController.get_all_players()
        player_dict = {p.id: p for p in all_players}
        scores = {pid: player_dict[pid].score for pid in tournament.players}
        sorted_players = sorted(tournament.players, key=lambda pid: (-scores[pid], random.random()))

        past_pairs = set()
        for round_ in tournament.rounds:
            for match in round_["matches"]:
                player1_id = match[0][0]
                player2_id = match[1][0]
                if player1_id is None or player2_id is None:
                    continue  # ignorer les matchs avec bye
                pair = tuple(sorted([player1_id, player2_id]))
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

        if len(used) < len(sorted_players):
            solo = [pid for pid in sorted_players if pid not in used][0]
            matches.append([[solo, 1.0], [None, 0.0]])

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
        tournaments = TournamentController.get_all_tournaments()
        for i, t in enumerate(tournaments):
            if t.id == tournament.id:
                tournaments[i] = tournament
                break

        TournamentRepository.save_tournaments(tournaments)
        return new_round, None

    @staticmethod
    def enter_results_for_round(tournament, match_results):
        """
        Record the results of the latest round's matches and update player scores.
        """
        all_players = TournamentController.get_all_players()
        player_dict = {p.id: p for p in all_players}

        for match, result in zip(tournament.rounds[-1]["matches"], match_results):
            match[0][1], match[1][1] = result
            if match[0][0] is not None:
                player_dict[match[0][0]].score += match[0][1]
            if match[1][0] is not None:
                player_dict[match[1][0]].score += match[1][1]

        PlayerRepository.save_players(list(player_dict.values()))
        tournament.rounds[-1]["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tournaments = TournamentController.get_all_tournaments()
        for i, t in enumerate(tournaments):
            if t.id == tournament.id:
                tournaments[i] = tournament
                break
        TournamentRepository.save_tournaments(tournaments)

    @staticmethod
    def get_tournament_rankings(tournament):
        """
        Get the current rankings of players in the tournament.
        """
        all_players = TournamentController.get_all_players()
        player_dict = {p.id: p for p in all_players}
        return sorted(
            [(player_dict[pid], player_dict[pid].score) for pid in tournament.players],
            key=lambda x: -x[1]
        )

    @staticmethod
    def close_tournament(tournament):
        """
        Close the tournament if all rounds are completed.
        """
        if any(r["end_time"] is None for r in tournament.rounds):
            return False
        tournament.is_closed = True
        TournamentRepository.save_tournaments(TournamentController.get_all_tournaments())
        return True

    @staticmethod
    def get_current_round(tournament):
        """
        Get the current active round (if not yet completed).
        """
        if not tournament.rounds:
            return None

        last_round = tournament.rounds[-1]
        if last_round["end_time"] is None:
            return last_round
        return None

    @staticmethod
    def set_match_result(match, score1, score2):
        """
        Set the result of a specific match and update the corresponding player scores.
        """
        match[0][1] = score1
        match[1][1] = score2

        all_players = PlayerRepository.load_players()
        player_dict = {p.id: p for p in all_players}

        if match[0][0] is not None:
            player_dict[match[0][0]].score += score1
        if match[1][0] is not None:
            player_dict[match[1][0]].score += score2

        PlayerRepository.save_players(list(player_dict.values()))

    @staticmethod
    def finalize_round(tournament):
        """
        Finalize the current round by setting its end time and saving the tournament.
        """
        if tournament.rounds:
            tournament.rounds[-1]["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tournaments = TournamentController.get_all_tournaments()
            for i, t in enumerate(tournaments):
                if t.id == tournament.id:
                    tournaments[i] = tournament
                    break
            TournamentRepository.save_tournaments(tournaments)

    @staticmethod
    def has_incomplete_rounds(tournament):
        """
        Check whether the tournament still has any ongoing (incomplete) rounds.
        """
        for round_ in tournament.rounds:
            if round_["end_time"] is None:
                return True
        return False

    @staticmethod
    def display_final_summary(tournament):
        """
        Display a summary of the tournament including location, dates,
        description, and final rankings.
        """
        print(f"\n🏁 Résumé final du tournoi « {tournament.name} »")
        print(f"📍 Lieu : {tournament.location}")
        print(f"📅 Dates : {tournament.start_date} → {tournament.end_date}")
        print(f"📝 Description : {tournament.description}\n")

        print("📊 Classement final :")
        rankings = TournamentController.get_tournament_rankings(tournament)
        for i, (player, score) in enumerate(rankings, start=1):
            print(f"  {i}. {player.first_name} {player.last_name} - {score} pts")

        print("\n✅ Le tournoi est maintenant clôturé.\n")
