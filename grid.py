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
            

    def next_grid(self, column, row):
        self.get_location(column, row)


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


    def play(self, player, column, row):
        column -= 1
        row -= 1

        location = self.get_location(column, row)
        mini_grid = self.grid[location]
        (row, column) = mini_grid.convert_coordinates(column, row) 

        return mini_grid.play(player, column, row)
        
            

    def print_grid(self):
        # 1. On définit la disposition visuelle des clés de ton dictionnaire
        layout = [
            ["top_left", "top_center", "top_right"],
            ["center_left", "center_center", "center_right"],
            ["bottom_left", "bottom_center", "bottom_right"]
        ]
        
        print()
        for i in range(3): # Parcourt le "layout" ligne par ligne (top, center, bottom)
            for j in range(3): # Parcourt les 3 lignes à l'intérieur des mini-grilles
                ligne = []
                for k in range(3): # Parcourt les 3 colonnes du "layout" (left, center, right)
                    
                    # On récupère le nom ("top_left", etc.)
                    location_name = layout[i][k]
                    # On va chercher la bonne mini-grille dans ton dictionnaire
                    mini_grid = self.grid[location_name]
                    # On extrait la ligne 'j' de cette mini-grille
                    cellules = mini_grid.grid[j]
                    
                    ligne.append(" " + " │ ".join(cellules) + " ")
                
                # On assemble la grande ligne avec la double barre ║
                print("║".join(ligne))
                
                # Séparateurs simples entre les lignes des petites grilles
                if j < 2:
                    print("───┼───┼───║───┼───┼───║───┼───┼───")   
            
            # Séparateurs doubles entre les grandes rangées (top/center/bottom)
            if i < 2:
                print("═══════════╬═══════════╬═══════════")
        print()
