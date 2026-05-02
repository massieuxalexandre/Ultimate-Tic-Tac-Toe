import math

class Player:
    # joueur humain, il a son nom et son symbole
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class AI(Player):
    # joueur AI, on ajoute sa profondeur d'élagage
    def __init__(self, name, symbol, depth):
        super().__init__(name, symbol)
        self.depth = depth

    def get_action(self, grid):
        # on retourne l'action que l'AI a décidé de faire (grâce au minimax avec la profondeur d'élagage choisie dans le main)
        return self.minimax(grid, self.depth)

    def minimax(self, grid, depth):
        # fonction minimax avec élagage alpha beta (comme vu en TD)
        alpha = -math.inf
        beta = math.inf
        actions_values = []

        for action in grid.get_possible_actions(): 
            score = self.min_value(self.result(grid, self, action), alpha, beta, depth - 1)
            actions_values.append((action, score))
            alpha = max(alpha, score)

        if not actions_values:
            return None
        
        best_action = max(actions_values, key=lambda x: x[1])
        # on retourne donc la meilleure action possible
        return best_action[0]
    

    def result(self, grid, player_obj, action):
        # on copie la grille acuelle, on regarde les conséquences des actions (on fait donc des simulations)
        simulation = grid.clone()
        simulation.play(player_obj, action[0], action[1])
        return simulation


    def max_value(self, grid, alpha, beta, depth):
        if grid.has_winner() or grid.is_full(): 
            return self.utility(grid)
        if depth == 0:
            return self.heuristique(grid)
        
        v = -math.inf

        for a in grid.get_possible_actions():
            v = max(v, self.min_value(self.result(grid, self, a), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v


    def min_value(self, grid, alpha, beta, depth):
        if grid.has_winner() or grid.is_full():
            return self.utility(grid)
        if depth == 0:
            return self.heuristique(grid)
        
        v = math.inf
        
        if self.symbol == 'X':
            opponent_symbol = 'O'
        else:
            opponent_symbol = 'X'

        opponent = Player("Simulated_opponent", opponent_symbol)
        
        for a in grid.get_possible_actions():
            v = min(v, self.max_value(self.result(grid, opponent, a), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)

        return v


    def utility(self, grid):
        # on définit l'importance de la victoire ou défaite
        if grid.winner == self.symbol: 
            return 10000  
        elif grid.winner is not None: 
            return -10000 
        return 0         


    def heuristique(self, grid):
        score = 0
        if self.symbol == 'X':
            opponent_symbol = 'O'
        else:
            opponent_symbol = 'X'

        # 1 - Nb de sous grilles gagnées (pour gagner un match nul grâce aux points
        for location, mini_grid in grid.grid.items():
            if mini_grid.winner == self.symbol:
                score += 150 # gros bonus 
            elif mini_grid.winner == opponent_symbol:
                score -= 150

        # 2 - contrôle du centre
        if grid.grid["center_center"].winner == self.symbol:
            score += 50
        elif grid.grid["center_center"].winner == opponent_symbol:
            score -= 50

        # 3 - alignements possibles sur la grande grille
        ultimates_alignments = [
            ["top_left", "top_center", "top_right"],
            ["center_left", "center_center", "center_right"],
            ["bottom_left", "bottom_center", "bottom_right"],
            ["top_left", "center_left", "bottom_left"],
            ["top_center", "center_center", "bottom_center"],
            ["top_right", "center_right", "bottom_right"],
            ["top_left", "center_center", "bottom_right"],
            ["top_right", "center_center", "bottom_left"]
        ]

        for aligment in ultimates_alignments:
            row = [grid.grid[loc].winner for loc in aligment]
            score += self.evaluate(row, self.symbol, opponent_symbol) * 100

        # 4 - alignements des sous grilles
        for location, mini_grid in grid.grid.items():
            if mini_grid.winner is None and not mini_grid.is_full():
                
                # contrôle du centre de la sous grille
                if mini_grid.grid[1][1] == self.symbol:
                    score += 5
                elif mini_grid.grid[1][1] == opponent_symbol:
                    score -= 5

                # check lignes
                for i in range(3):
                    score += self.evaluate(mini_grid.grid[i], self.symbol, opponent_symbol)
                
                # check colonnes
                for j in range(3):
                    col = [mini_grid.grid[0][j], mini_grid.grid[1][j], mini_grid.grid[2][j]]
                    score += self.evaluate(col, self.symbol, opponent_symbol)
                
                # check diagonales
                diag1 = [mini_grid.grid[0][0], mini_grid.grid[1][1], mini_grid.grid[2][2]]
                diag2 = [mini_grid.grid[0][2], mini_grid.grid[1][1], mini_grid.grid[2][0]]
                score += self.evaluate(diag1, self.symbol, opponent_symbol)
                score += self.evaluate(diag2, self.symbol, opponent_symbol)

        return score


    def evaluate(self, row, ai_symbol, opp_symbol):
        # on définit l'importance d'un coup selon les cases occupées (par le joueur adverse ou l'ia elle-même)
        score = 0
        nb_ai = row.count(ai_symbol)
        nb_opp = row.count(opp_symbol)

        if nb_ai > 0 and nb_opp == 0:
            if nb_ai == 3:
                score += 100 
            elif nb_ai == 2:
                score += 10
            elif nb_ai == 1:
                score += 1

        elif nb_opp > 0 and nb_ai == 0:
            if nb_opp == 3:
                score -= 100
            elif nb_opp == 2:
                score -= 10
            elif nb_opp == 1:
                score -= 1

        return score