from player import Player, AI
from grid import Grid, UltimateGrid
from utils import *

def main():
    mini_grids_locations = ["top_left", "top_center", "top_right",
        "center_left", "center_center", "center_right", 
        "bottom_left", "bottom_center", "bottom_right"
    ]
    player_1 = Player("Humain", 'X')
    # player_2 = Player("AI", 'O')
    player_2 = AI("AI", 'O', 3)
    players = [player_1, player_2]
    
    ultimate_grid = UltimateGrid(mini_grids_locations, player_1, player_2)

    print("Bienvenue dans Ultimate Tic Tac Toe")
    print("Qui commence la partie ? :")
    print("1.", player_1.name)
    print("2.", player_2.name)
    print()
    start_choice = str(input())

    while not valid_choice(start_choice, 1, 2):
        print("Choix invalide, veuillez réessayer.")
        start_choice = str(input())
        clear()

    if start_choice == "1":
        tour = 0

    elif start_choice == "2":
        tour = 1
    
    clear()
    ultimate_grid.print_grid()



    while not ultimate_grid.is_full() and not ultimate_grid.has_winner():
        if (tour % 2 == 0):
            player = players[0]
        else:
            player = players[1]


        if ultimate_grid.next_grid != None:
            print(player.name, "doit jouer dans la grille", ultimate_grid.next_grid)
        else:
            print(player.name, "peut jouer dans n'importe quelle grille")

        if isinstance(player, AI):
            action = player.get_action(ultimate_grid)
            column, row = action[0], action[1]

        else:
            print("Colonne : ", end='')
            column = str(input())
            if not valid_choice(column, 1, 9):
                clear()
                ultimate_grid.print_grid()
                print("Colonne invalide, veuillez réessayer")
                print()
                continue
            
            print("Ligne : ", end='')
            row = str(input())
            clear()
            if not valid_choice(row, 1, 9):
                clear()
                ultimate_grid.print_grid()
                print("Ligne invalide, veuillez réessayer")
                print()
                continue

        if not ultimate_grid.play(player, int(column), int(row)):
            clear()
            ultimate_grid.print_grid()
            if ultimate_grid.next_grid != None:
                print("Veuillez réessayer, ", end='')
            else:
                print("Case déjà occupée, veuillez réessayer")
                print()
            continue
        else:
            clear()
            print(player.name, "a joué en colonne", column, "et ligne", row)
            
        ultimate_grid.print_grid()
        tour += 1


    if ultimate_grid.has_winner():
        print("Le gagnant est", ultimate_grid.winner)
    else:
        print("Match nul !")


if __name__ == "__main__":
    main()