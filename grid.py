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




class UltimateGrid():
    def __init__(self, mini_grids_locations, player_1, player_2):
        self.grid = list()
        for i in range(3):
            row = []
            for j in range(3):
                row.append(Grid(mini_grids_locations[i][j], player_1, player_2))
            self.grid.append(row)
        
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = None
        self.is_full = False



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