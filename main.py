from player import Player
from grid import Grid, UltimateGrid
from utils import *

def main():
    mini_grids_locations = ["top_left", "top_center", "top_right",
        "center_left", "center_center", "center_right", 
        "bottom_left", "bottom_center", "bottom_right"
    ]
    player = Player("Alex", 'X')
    ai = Player("AI", 'O')
    
    ultimate_grid = UltimateGrid(mini_grids_locations, player, ai)

    print("Qui commence la partie ? :")
    print("1.", player.name)
    print("2.", ai.name)
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

    row_mini = "1"
    row_maxi = "9"
    column_mini = "1"
    column_maxi = "9"
    while True:
        if (tour % 2 == 0):
            print("C'est à", player.name, "de jouer")
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
                print("Case déjà occupée, veuillez réessayer")
                print()
                continue
            else:
                print(player.name, "a joué en colonne", column, "et ligne", row)

        else:
            print("C'est à", ai.name, "de jouer")
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
            if not valid_choice(row, 1, 9):
                clear()
                ultimate_grid.print_grid()
                print("Ligne invalide, veuillez réessayer")
                print()
                continue
            clear()

            if not ultimate_grid.play(ai, int(column), int(row)):
                clear()
                ultimate_grid.print_grid()
                print("Case déjà occupée, veuillez réessayer")
                print()
                continue
            else:
                print(ai.name, "a joué en colonne", column, "et ligne", row)
            
        ultimate_grid.print_grid()
        
        tour += 1




if __name__ == "__main__":
    main()