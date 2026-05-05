from player import Player, AI
from grid import UltimateGrid
from utils import *

def main():
    # création de 2 joueurs (1 humain qui sera l'utilisateur et 1 ia)
    human = Player("Humain", 'X')
    # ai = Player("AI", 'O')
    ai = AI("AI", 'O', 7)
    
    # création de la grille principale contenant 9 sous grilles (jouée par les 2 joueurs)
    mini_grids_locations = ["top_left", "top_center", "top_right",
                            "center_left", "center_center", "center_right", 
                            "bottom_left", "bottom_center", "bottom_right"
    ]
    ultimate_grid = UltimateGrid(mini_grids_locations, human, ai)

    # choisir qui commence la partie (on prend un string pour gérer plus facilement une erreur de frappe)
    print("Bienvenue dans Ultimate Tic Tac Toe")
    print("Qui commence la partie ? :")
    print("1.", human.name)
    print("2.", ai.name)
    print()
    start_choice = str(input())

    # fonctino "valid_choice" dans utils.py. Elle permet de checker si le choix de l'utilisateur est valide ou non (compris parmi un bornage)
    while not valid_choice(start_choice, 1, 2):
        print("Choix invalide, veuillez réessayer.")
        start_choice = str(input())
        print()

    if start_choice == "1":
        tour = 0

    elif start_choice == "2":
        tour = 1
    
    clear()
    ultimate_grid.print_grid()

    # boucle principale. tant que la grille n'est pas remplie et pas de gagnant 
    while not ultimate_grid.is_full() and not ultimate_grid.has_winner():
        if (tour % 2 == 0):
            # tour pair = tour de l'humain
            player = human
        else:
            # tour impair = tour de l'ai
            player = ai

        # on dit au joueur dans quelle sous grille il doit jouer
        if ultimate_grid.next_grid != None:
            print(player.name, "doit jouer dans la grille", ultimate_grid.next_grid)
        else:
            print(player.name, "peut jouer dans n'importe quelle grille")

        # si c'est au tour de l'AI, il joue tout seul (grâce au minimax + élagage alpha beta)
        if isinstance(player, AI):
            action = player.get_action(ultimate_grid)
            column, row = action[0], action[1]


        # si c'est au tour du joueur, il choisit où il joue (colonne puis ligne)
        # on prend l'input en string pour gérer les erreurs plus facilement avec la fonction valid_choice
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

        # si la case choisie par l'utilisateur n'est pas possible, on affiche l'erreur
        if not ultimate_grid.play(player, int(column), int(row)):
            clear()
            ultimate_grid.print_grid()
            if ultimate_grid.next_grid != None:
                print("Veuillez réessayer, ", end='')
            else:
                print("Case déjà occupée, veuillez réessayer")
                print()
            continue

        # sinon il peut bien jouer donc on affiche ce qu'il a joué
        else:
            clear()
            print(player.name, "a joué en colonne", column, "et ligne", row)
            
        # affichage de la grille puis on passe au tour suivant
        ultimate_grid.print_grid()
        tour += 1


    # fin de boucle = grille complète ou gagnée
    clear()
    ultimate_grid.print_grid()
    print("Fin de la partie !")

    # s'il y a un gagnant, on l'affiche
    if ultimate_grid.has_winner():
        if ultimate_grid.winner == human.symbol:
            print("Victoire de :", human.name)
        else:
            print("Victoire de :", ai.name)
    else:
        # si match nul sur la grande grille, on compte les sous grilles gagnées
        points_p1 = 0
        points_p2 = 0
        
        for location, mini_grid in ultimate_grid.grid.items():
            if mini_grid.winner == human.symbol:
                points_p1 += 1
            elif mini_grid.winner == ai.symbol:
                points_p2 += 1
                
        print("Match nul sur les alignements, comptage des sous grilles remportées :")
        print(human.name, ":", points_p1,  "grilles")
        print(ai.name, ":", points_p2,  "grilles")
        
        if points_p1 > points_p2:
            print("Victoire aux points pour", human.name, "!")
        elif points_p2 > points_p1:
            print("Victoire aux points pour", ai.name, "!")

        # si autant de sous grilles gagnées pour l'un que pour l'autre => égalité parfaite
        else:
            print("Égalité parfaite")

        print()


if __name__ == "__main__":
    main()