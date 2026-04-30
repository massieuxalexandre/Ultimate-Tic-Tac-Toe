from player import Player


class Grid:
    def __init__(self, location, player_1, player_2):
        self.location = location
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = None


    def play(self, player, column, row):
        if self.grid[row][column] in ['X', 'O']:
            return False

        self.grid[row][column] = player.symbol
        return True


    def print_grid(self):
        for i, row in enumerate(self.grid):
            print(" " + " | ".join(row))
            if i < 2:
                print("---+---+---")

    def convert_coordinates(self, ultimate_column, ultimate_row):
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
        # Optimisation : si on a déjà détecté un gagnant, court-circuiter
        if self.winner is not None:
            return True

        g = self.grid
        # Lignes
        for row in g:
            if row[0] == row[1] == row[2] != ' ':
                self.winner = row[0]
                return True
        # Colonnes
        for col in range(3):
            if g[0][col] == g[1][col] == g[2][col] != ' ':
                self.winner = g[0][col]
                return True
        # Diagonales
        if g[0][0] == g[1][1] == g[2][2] != ' ':
            self.winner = g[0][0]
            return True
        if g[0][2] == g[1][1] == g[2][0] != ' ':
            self.winner = g[0][2]
            return True

        return False


    def is_full(self):
        for row in self.grid:
            if ' ' in row:
                return False
        return True


class UltimateGrid(Grid):
    def __init__(self, mini_grids_locations, player_1, player_2):
        Grid.__init__(self, "ultimate_grid", player_1, player_2)
        self.grid = dict()
        for location in mini_grids_locations:
            self.grid[location] = Grid(location, player_1, player_2)

        self.next_grid = None


    def play(self, player, column, row):
        column -= 1
        row -= 1

        target_location = self.get_location(column, row)

        if self.next_grid is not None and self.next_grid != target_location:
            return False

        mini_grid = self.grid[target_location]
        if mini_grid.has_winner() or mini_grid.is_full():
            return False
        (row, column) = mini_grid.convert_coordinates(column, row)

        if mini_grid.play(player, column, row):
            if mini_grid.winner is None:
                mini_grid.has_winner()

            self.next_grid = mini_grid.find_next_grid(column, row)
            if self.grid[self.next_grid].is_full() or self.grid[self.next_grid].has_winner():
                self.next_grid = None
            return True

        return False

    # ---------------- AI helpers : make/undo (zéro deepcopy) ----------------
    def make_move(self, player, column, row):
        """
        Joue un coup ET renvoie un objet `undo` qu'on peut passer à
        `undo_move()` pour annuler complètement l'effet du coup.
        Renvoie None si le coup est invalide.

        Bien plus rapide que deepcopy : aucune allocation de structure,
        on stocke juste l'état précédent des champs modifiés.
        """
        col0 = column - 1
        row0 = row - 1
        target_location = self.get_location(col0, row0)

        if self.next_grid is not None and self.next_grid != target_location:
            return None

        mini_grid = self.grid[target_location]
        if mini_grid.winner is not None or mini_grid.is_full():
            return None

        local_row, local_col = mini_grid.convert_coordinates(col0, row0)
        if mini_grid.grid[local_row][local_col] != ' ':
            return None

        # On sauvegarde tout ce qui peut changer
        undo = (
            target_location,
            local_row, local_col,
            mini_grid.winner,
            self.next_grid,
            self.winner,
        )

        # Application
        mini_grid.grid[local_row][local_col] = player.symbol

        # Mise à jour du gagnant de la mini-grille (peut rester None)
        if mini_grid.winner is None:
            mini_grid.has_winner()

        # Sous-grille suivante
        nxt = mini_grid.find_next_grid(local_col, local_row)
        if nxt is not None:
            ng = self.grid[nxt]
            if ng.winner is not None or ng.is_full():
                nxt = None
        self.next_grid = nxt

        # Mise à jour du gagnant global
        if self.winner is None:
            self.has_winner()

        return undo

    def undo_move(self, undo):
        """Annule un coup joué via make_move()."""
        target_location, local_row, local_col, old_mini_winner, old_next_grid, old_meta_winner = undo
        mini_grid = self.grid[target_location]
        mini_grid.grid[local_row][local_col] = ' '
        mini_grid.winner = old_mini_winner
        self.next_grid = old_next_grid
        self.winner = old_meta_winner
    # ----------------------------------------------------------------------

    def is_full(self):
        for location in self.grid:
            mini_grid = self.grid[location]
            # Si la sous-grille n'est pas pleine et n'a pas de gagnant
            if not mini_grid.is_full() and mini_grid.winner is None:
                return False
        return True



    def has_winner(self):
        # Optimisation : court-circuiter si déjà connu
        if self.winner is not None:
            return True

        g = self.grid
        # Lignes du méta-plateau
        for trio in (
            ("top_left", "top_center", "top_right"),
            ("center_left", "center_center", "center_right"),
            ("bottom_left", "bottom_center", "bottom_right"),
            ("top_left", "center_left", "bottom_left"),
            ("top_center", "center_center", "bottom_center"),
            ("top_right", "center_right", "bottom_right"),
            ("top_left", "center_center", "bottom_right"),
            ("top_right", "center_center", "bottom_left"),
        ):
            w0 = g[trio[0]].winner
            if w0 is not None and w0 == g[trio[1]].winner == g[trio[2]].winner:
                self.winner = w0
                return True

        return False


    def get_possible_actions(self):
        actions = []
        next_grid = self.next_grid
        for col in range(1, 10):
            for row in range(1, 10):
                target_location = self.get_location(col-1, row-1)
                if next_grid is not None and next_grid != target_location:
                    continue
                mini_grid = self.grid[target_location]
                if mini_grid.winner is not None or mini_grid.is_full():
                    continue

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

        # Motifs  pour remplacer les grilles gagnées
        # Chaque liste contient 3 lignes de 3 caractères
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
