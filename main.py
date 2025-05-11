from views.player_view import create_player_view, list_players_view


def main_menu():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Ajouter un joueur")
        print("2. Afficher les joueurs")
        print("3. Quitter")

        choice = input("Votre choix : ").strip()

        if choice == "1":
            create_player_view()
        elif choice == "2":
            list_players_view()
        elif choice == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Réessayez.")


if __name__ == "__main__":
    main_menu()
