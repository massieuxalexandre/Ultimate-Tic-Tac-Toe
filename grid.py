from player import Player

class Grid:
    # classe correspondant à une sous grille
    # donc une grille de morpion classique
    def __init__(self, location, player_1, player_2):
        self.location = location
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = None


    def play(self, player, column, row):
        # si la case est déjà jouée, on return false
        if self.grid[row][column] in ['X', 'O']:
            return False
        
        # sinon on peut jouer
        self.grid[row][column] = player.symbol
        return True
    

    def clone(self):
        # fonction pour copier une grille pour que l'AI puisse jouer/tester dessus sans modifier celle actuelle
        new_grid = Grid(self.location, self.player_1, self.player_2)
        new_grid.grid = [row[:] for row in self.grid] 
        new_grid.winner = self.winner
        return new_grid
    

    def print_grid(self):
        # affichage d'une sous geille
        for i, row in enumerate(self.grid):
            print(" " + " | ".join(row))
            if i < 2:
                print("---+---+---")
            

    def convert_coordinates(self, ultimate_column, ultimate_row):
        # convertion des coordonées entrées par le joueur en celles d'une sous grille (donc de 0 à 2)
        if self.location in ["top_left", "center_left", "bottom_left"]:
            column = ultimate_column
        elif self.location in ["top_center", "center_center", "bottom_center"]:
            column = ultimate_column - 3
        else:
            column = ultimate_column - 6

        if self.location in ["top_left", "top_center", "top_right"]:
            row = ultimate_row
        elif self.location in ["center_left", "center_center", "center_right"]:
            row = ultimate_row - 3
        else:
            row = ultimate_row - 6

        return (row, column)
    

    def get_location(self, column, row):
        # retourne quelle sous grille
        if column < 3:
            if row < 3:
                return "top_left"
            elif row < 6:
                return "center_left"
            else:
                return "bottom_left"
        elif column < 6:
            if row < 3:
                return "top_center"
            elif row < 6:
                return "center_center"
            else:
                return "bottom_center"
        else:
            if row < 3:
                return "top_right"
            elif row < 6:
                return "center_right"
            else:
                return "bottom_right"
            

    def find_next_grid(self, column, row):
        # returne quelle sous grille doit être jouée au tour d'après en fonction de la case jouée actuellement
        if (column, row) == (0, 0):
            return "top_left"
        elif (column, row) == (1, 0):
            return "top_center"
        elif (column, row) == (2, 0):
            return "top_right"
        elif (column, row) == (0, 1):
            return "center_left"
        elif (column, row) == (1, 1):
            return "center_center"
        elif (column, row) == (2, 1):
            return "center_right"
        elif (column, row) == (0, 2):
            return "bottom_left"
        elif (column, row) == (1, 2):
            return "bottom_center"
        elif (column, row) == (2, 2):
            return "bottom_right"
        else:
            return None
        

    def has_winner(self):
        # on vérifie si cette grille est remportée

        # check lignes
        for row in self.grid:
            if row[0] == row[1] == row[2] != ' ':
                self.winner = row[0]
                return True
            
        # check colonenes
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != ' ':
                self.winner = self.grid[0][col]
                return True

        # check diagonales
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != ' ':
            self.winner = self.grid[0][0]
            return True
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ' ':
            self.winner = self.grid[0][2]
            return True

        return False


    def is_full(self):
        # on vérifie si cette grille est complète (donc on regarde s'il reste des cases vides)
        for row in self.grid:
            if ' ' in row:
                return False
        return True


class UltimateGrid(Grid):
    # grille principales contenant 9 sous grilles (Grid)
    def __init__(self, mini_grids_locations, player_1, player_2):
        Grid.__init__(self, "ultimate_grid", player_1, player_2)

        # dictionnaire car par la suite, on pourra appeler les sous grilles par leur nom (leur localisation) directement
        self.grid = dict()
        for location in mini_grids_locations:
            self.grid[location] = Grid(location, player_1, player_2)

        self.next_grid = None


    def play(self, player, column, row):
        # conversion des coordonées entrées par le joueur en index 
        column -= 1
        row -= 1

        # on définit dans quelle sous grille le joueur est en train de jouer
        target_location = self.get_location(column, row)

        # si le joueur ne joue pas dans la sous grille qui lui est contrainte, alors il ne peut pas joeur = return false
        if self.next_grid != None and self.next_grid != target_location:
            return False

        # on récupère la sous grille dans laquelle le joueur joue
        mini_grid = self.grid[target_location]

        # si cette sous grille est remportée ou complète, on ne peut pas jouer
        if mini_grid.has_winner() or mini_grid.is_full():
            return False
        
        # conversion des coordonées de la grande grille à celle de la sous grille jouée (de 0 à 2)
        (row, column) = mini_grid.convert_coordinates(column, row) 

        # on joue dans la mini grille
        if mini_grid.play(player, column, row):
            # on check si la sous grille est remportée grâce à la fonction has_winner()
            if mini_grid.winner is None:
                mini_grid.has_winner()
            
            # on définit dans quelle sous grille le joueur du tour suivant doit jouer
            self.next_grid = mini_grid.find_next_grid(column, row)
            # si celle-ci est déjà remportée ou complète, alors le joueur pourra jouer n'importe où
            if self.grid[self.next_grid].is_full() or self.grid[self.next_grid].has_winner():
                self.next_grid = None

            return True
        
        # si on n'a pas pu jouer dans la mini grille (car case déjà occupée), alors on ne peut pas jouer
        return False
    

    def clone(self):
        # fonction pour copier une grille pour que l'AI puisse jouer/tester dessus sans modifier celle actuelle
        new_ultimate = UltimateGrid([], self.player_1, self.player_2)
        new_ultimate.grid = dict()
        for location, mini_grid in self.grid.items():
            new_ultimate.grid[location] = mini_grid.clone()
        new_ultimate.next_grid = self.next_grid
        new_ultimate.winner = self.winner
        return new_ultimate
        
            
    def is_full(self):
        # on vérifie si cette grille principale est complète (donc on regarde si toutes les mini grilles sont complètes)
        for location in self.grid:
            mini_grid = self.grid[location]
            # si la sous-grille n'est pas pleine et n'a pas de gagnant
            if not mini_grid.is_full() and mini_grid.winner is None:
                return False
        return True
    

    
    def has_winner(self):
        # on vérifie si cette grille principale a un gagnant

        # on check les lignes
        for row in range(0, 9, 3):
            if self.grid[self.get_location(0, row)].has_winner() and self.grid[self.get_location(3, row)].has_winner() and self.grid[self.get_location(6, row)].has_winner():
                if self.grid[self.get_location(0, row)].winner == self.grid[self.get_location(3, row)].winner == self.grid[self.get_location(6, row)].winner:
                    self.winner = self.grid[self.get_location(0, row)].winner
                    return True
        
        # on check les colonnes
        for col in range(0, 9, 3):
            if self.grid[self.get_location(col, 0)].has_winner() and self.grid[self.get_location(col, 3)].has_winner() and self.grid[self.get_location(col, 6)].has_winner():
                if self.grid[self.get_location(col, 0)].winner == self.grid[self.get_location(col, 3)].winner == self.grid[self.get_location(col, 6)].winner:
                    self.winner = self.grid[self.get_location(col, 0)].winner
                    return True

        # on check les diagonales
        if self.grid[self.get_location(0, 0)].has_winner() and self.grid[self.get_location(3, 3)].has_winner() and self.grid[self.get_location(6, 6)].has_winner():
            if self.grid[self.get_location(0, 0)].winner == self.grid[self.get_location(3, 3)].winner == self.grid[self.get_location(6, 6)].winner:
                self.winner = self.grid[self.get_location(0, 0)].winner
                return True
        if self.grid[self.get_location(0, 6)].has_winner() and self.grid[self.get_location(3, 3)].has_winner() and self.grid[self.get_location(6, 0)].has_winner():
            if self.grid[self.get_location(0, 6)].winner == self.grid[self.get_location(3, 3)].winner == self.grid[self.get_location(6, 0)].winner:
                self.winner = self.grid[self.get_location(0, 6)].winner
                return True
        

    def get_possible_actions(self):
        # fonction pour l'AI, on retourne toutes les actions possibles dans l'état actuel
        actions = []
        # on regarde pour toutes les cases (de (1, 1) à (9, 9))
        for col in range(1, 10):
            for row in range(1, 10):
                # on regarde à quelle sous grille correspond la case (convertion en index)
                target_location = self.get_location(col-1, row-1)

                # si cette case n'est pas dans la sous grille contrainte, on passe à la case suivante
                if self.next_grid != None and self.next_grid != target_location:
                    continue

                # sinon on regarde cette sous grille en détail
                mini_grid = self.grid[target_location]
                # sauf si elle est full ou si elle a un gagnant, on passe à la case suivante
                if mini_grid.has_winner() or mini_grid.is_full():
                    continue

                # si cette case est vide, on l'ajoute à la liste des actions possibles
                (locals_row, local_col) = mini_grid.convert_coordinates(col-1, row-1)
                if mini_grid.grid[locals_row][local_col] == ' ':
                    actions.append((col, row))

        return actions


    def print_grid(self):
        layout = [
            ["top_left", "top_center", "top_right"],
            ["center_left", "center_center", "center_right"],
            ["bottom_left", "bottom_center", "bottom_right"]
        ]
        
        # Motifs  pour remplacer les grilles gagnées (plus lisible)
        big_X = [
            [' ', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' ']
        ]
        
        big_O = [
            [' ', ' ', ' '],
            [' ', 'O', ' '],
            [' ', ' ', ' ']
        ]

        print()
        print("    1   2   3   4   5   6   7   8   9")
        
        for i in range(3): # Blocs de 3 grilles (Lignes macro)
            for j in range(3): # Lignes à l'intérieur des mini-grilles
                ligne_complete = []
                for k in range(3): # Colonnes macro
                    location_name = layout[i][k]
                    mini_grid = self.grid[location_name]
                    
                    # CONDITION D'AFFICHAGE SPÉCIALE
                    if mini_grid.winner == 'X':
                        # On affiche la ligne 'j' du motif géant X
                        cellules = big_X[j]
                        # On enlève les barres internes "│" en mettant des espaces
                        ligne_complete.append(" " + "   ".join(cellules) + " ")
                    
                    elif mini_grid.winner == 'O':
                        # On affiche la ligne 'j' du motif géant O
                        cellules = big_O[j]
                        # On enlève les barres internes "│" en mettant des espaces
                        ligne_complete.append(" " + "   ".join(cellules) + " ")
                    
                    else:
                        # Affichage normal avec les barres de séparation
                        cellules = mini_grid.grid[j]
                        ligne_complete.append(" " + " │ ".join(cellules) + " ")
                
                numero_ligne = i * 3 + j + 1
                print(f" {numero_ligne} " + "║".join(ligne_complete))
                
                if j < 2:
                    # On ajuste le séparateur pour qu'il soit invisible là où une grille est gagnée
                    separateurs = []
                    for k in range(3):
                        if self.grid[layout[i][k]].winner:
                            separateurs.append("           ") # Vide si gagné
                        else:
                            separateurs.append("───┼───┼───") # Normal
                    print("   " + "║".join(separateurs))
            
            if i < 2:
                print("   ═══════════╬═══════════╬═══════════")
        print()
