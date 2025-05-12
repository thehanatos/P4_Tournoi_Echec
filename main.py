from views.player_view import create_player_view, list_players_view
from views.tournament_view import (
    create_tournament_view,
    list_tournaments_view,
    register_players_to_tournament_view,
    show_players_in_tournament_view,
    start_new_round_view,
    enter_results_for_round_view
)


def main_menu():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Ajouter un joueur")
        print("2. Afficher les joueurs")
        print("3. Créer un tournoi")
        print("4. Afficher les tournois")
        print("5. Inscrire des joueurs dans un tournoi")
        print("6. Voir les joueurs d’un tournoi")
        print("7. Démarrer un round")
        print("8. Entrer les résultats d’un round")
        print("9. Quitter")

        choice = input("Votre choix : ").strip()

        if choice == "1":
            create_player_view()
        elif choice == "2":
            list_players_view()
        elif choice == "3":
            create_tournament_view()
        elif choice == "4":
            list_tournaments_view()
        elif choice == "5":
            register_players_to_tournament_view()
        elif choice == "6":
            show_players_in_tournament_view()
        elif choice == "7":
            start_new_round_view()
        elif choice == "8":
            enter_results_for_round_view()
        elif choice == "9":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Réessayez.")


if __name__ == "__main__":
    main_menu()
