from player import Player


class Grid:
    def __init__(self, location, player_1, player_2):
        self.location = location
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = None
        self.is_full = False
        self.next_grid = None


    def print_grid(self):
        print()
        for i, row in enumerate(self.grid):
            print(" " + " | ".join(row))
            if i < 2:
                print("---+---+---")
            
    def convert_coordinates(self, ultimate_column, ultimate_row):
        if self.location == "top_left":
            return (ultimate_row, ultimate_column)
        elif self.location == "top_center":
            return (ultimate_row, ultimate_column + 3)
        elif self.location == "top_right":
            return (ultimate_row, ultimate_column + 6)
        elif self.location == "center_left":
            return (ultimate_row + 3, ultimate_column)
        elif self.location == "center_center":
            return (ultimate_row + 3, ultimate_column + 3)
        elif self.location == "center_right":
            return (ultimate_row + 3, ultimate_column + 6)
        elif self.location == "bottom_left":
            return (ultimate_row + 6, ultimate_column)
        elif self.location == "bottom_center":
            return (ultimate_row + 6, ultimate_column + 3)
        elif self.location == "bottom_right":
            return (ultimate_row + 6, ultimate_column + 6)


class UltimateGrid(Grid):
    def __init__(self, mini_grids_locations, player_1, player_2):
        Grid.__init__(self, "ultimate_grid", player_1, player_2)
        self.grid = list()
        for i in range(3):
            row = []
            for j in range(3):
                row.append(Grid(mini_grids_locations[i][j], player_1, player_2))
            self.grid.append(row)



    def print_grid(self):
            print()
            for i in range(3): 
                for j in range(3):
                    row = []
                    for k in range(3):
                        cells = self.grid[i][k].grid[j]
                        row.append(" " + " │ ".join(cells) + " ")
                    print("║".join(row))
                    if j < 2:
                        print("───┼───┼───║───┼───┼───║───┼───┼───")   
                if i < 2:
                    print("═══════════╬═══════════╬═══════════")
            print()

    def wich_mini_grid(self, column, row):
        return