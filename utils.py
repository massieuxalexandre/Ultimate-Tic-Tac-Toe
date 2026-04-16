from player import Player
from grid import Grid, UltimateGrid


def play(player, grid, column, row):
    column -= 1
    row -= 1

    if not isinstance(grid, UltimateGrid):
        (row, column) = grid.convert_coordinates(column, row)
        if grid.grid[row][column] == 'X' or grid.grid[row][column] == 'O':
            return False
        grid.grid[row][column] = player.symbol
        return True
        
    if grid.grid.grid[row][column] == 'X' or grid.grid.grid[row][column] == 'O':
        return False
        
    grid.grid.grid[row][column] = player.symbol
    return True


# def first_play(player, ultimate_grid, column, row):
#     column = int(column) - 1
#     row = int(row) - 1
#     if ultimate_grid.grid[row][column] == 'X' or ultimate_grid.grid[row][column] == 'O':
#         return False
    
#     ultimate_grid.grid[row][column] = player.symbol
#     return True


def clear():
    for i in range(100):
        print()

def valid_choice(choice, start, end):
    arr = list()
    for i in range(start, end+1):
        arr.append(str(i))

    return choice in arr