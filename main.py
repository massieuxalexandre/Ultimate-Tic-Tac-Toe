from player import Player
from grid import Grid, UltimateGrid

def main():
    mini_grids_locations = [
        ["top_left", "top_center", "top_right"],
        ["center_left", "center_center", "center_right"], 
        ["bottom_left", "bottom_center", "bottom_right"]
    ]
    player = Player("Moi", 'O')
    ai = Player("AI", 'X')
    
    ultimate_grid = UltimateGrid(mini_grids_locations, player, ai)
    # ultimate_grid.print_grid()

    while True:
        tour = 1
        print("Qui commence la partie ? :")
        print("1.", player.name)
        print("2.", ai.name)
        print()
        str(input())

        


if __name__ == "__main__":
    main()