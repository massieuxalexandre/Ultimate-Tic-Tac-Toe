import math


# ====================================================================
# Constantes pré-calculées (évite les recalculs dans les boucles chaudes)
# ====================================================================

# Ordre fixe des 9 mini-grilles (utilisé pour indexer les vecteurs d'état)
META_ORDER = (
    "top_left",    "top_center",    "top_right",
    "center_left", "center_center", "center_right",
    "bottom_left", "bottom_center", "bottom_right",
)

# Les 8 alignements gagnants sur un plateau 3x3 (indices dans META_ORDER)
LINES_3x3 = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # lignes
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # colonnes
    (0, 4, 8), (2, 4, 6),              # diagonales
)

# Poids positionnels d'une cellule à l'intérieur d'une mini-grille.
# Le centre est dans 4 lignes (max), les coins dans 3, les bords dans 2.
CELL_WEIGHTS = (
    (3, 2, 3),
    (2, 4, 2),
    (3, 2, 3),
)

# Poids positionnels d'une mini-grille dans le méta-plateau.
# Même logique : la mini-grille centrale est dans plus d'alignements.
META_WEIGHTS = (
    3, 2, 3,
    2, 4, 2,
    3, 2, 3,
)


def _line_score(my, opp):
    """
    Score d'une ligne de 3 cases en fonction de mes pions et ceux de l'adversaire.
    - Une ligne contenant les deux symboles est neutralisée (score 0).
    - Plus on a de pions seuls, plus c'est fort, exponentiellement.
    """
    if my and opp:
        return 0
    if my == 3:
        return 1000
    if my == 2:
        return 50          # menace forte (1 case manquante)
    if my == 1:
        return 5
    if opp == 3:
        return -1000
    if opp == 2:
        return -50
    if opp == 1:
        return -5
    return 0


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class AI(Player):
    """
    IA pour Ultimate Tic Tac Toe.

    Améliorations majeures par rapport à la version initiale :
    - Plus de `copy.deepcopy` : on utilise un mécanisme make/undo,
      ~50-100x plus rapide.
    - Bug critique corrigé : l'ancien code utilisait `'0'` (chiffre) au
      lieu de `'O'` (lettre) comme symbole adverse simulé quand l'IA
      jouait 'X' ; l'IA croyait littéralement que l'adversaire ne pouvait
      jamais gagner.
    - Heuristique stratégique :
        * pondération positionnelle des cellules (centre > coins > bords)
        * pondération des mini-grilles (centrale = plus de valeur)
        * détection des menaces et des doubles menaces
        * lignes mixtes correctement neutralisées
        * forte valorisation des mini-grilles déjà gagnées
        * récompense d'une victoire « aux points » sur match nul
    - Tri des coups (move ordering) au niveau de la racine et aux niveaux
      profonds : l'élagage alpha-bêta devient beaucoup plus efficace.
    - Court-circuit terminal et coup d'ouverture (centre du centre).
    """

    def __init__(self, name, symbol, depth):
        super().__init__(name, symbol)
        self.depth = depth
        self.opp_symbol = 'O' if symbol == 'X' else 'X'
        # Adversaire simulé (créé une seule fois, partagé dans toute la recherche)
        self._sim_opponent = Player("__sim_opponent__", self.opp_symbol)

    # ------------------------------------------------------------------
    # API publique
    # ------------------------------------------------------------------
    def get_action(self, grid):
        # Coup d'ouverture : si le plateau est totalement vide, jouer le
        # centre du centre, le coup le plus fort en théorie.
        if self._is_empty_board(grid):
            return (5, 5)

        actions = grid.get_possible_actions()
        if not actions:
            return None
        if len(actions) == 1:
            return actions[0]

        return self._search_root(grid, self.depth)

    # ------------------------------------------------------------------
    # Recherche minimax + alpha-bêta avec tri des coups
    # ------------------------------------------------------------------
    def _search_root(self, grid, depth):
        actions = grid.get_possible_actions()

        # Tri initial par évaluation 1-ply : on essaie d'abord les coups
        # qui semblent prometteurs -> meilleur élagage.
        actions = self._order_moves(grid, actions, maximizing=True)

        alpha = -math.inf
        beta = math.inf
        best_action = actions[0]
        best_score = -math.inf

        for action in actions:
            undo = grid.make_move(self, action[0], action[1])
            if undo is None:
                continue
            score = self._min_value(grid, alpha, beta, depth - 1)
            grid.undo_move(undo)

            if score > best_score:
                best_score = score
                best_action = action
            if score > alpha:
                alpha = score

        return best_action

    def _max_value(self, grid, alpha, beta, depth):
        if grid.winner is not None or grid.has_winner():
            return self._utility(grid)
        if grid.is_full():
            return self._utility(grid)
        if depth == 0:
            return self._heuristique(grid)

        actions = grid.get_possible_actions()
        if not actions:
            return self._heuristique(grid)

        # Tri des coups uniquement aux niveaux profonds (sinon le coût du
        # tri dépasse le gain en élagage).
        if depth >= 3 and len(actions) > 4:
            actions = self._order_moves(grid, actions, maximizing=True)

        v = -math.inf
        for action in actions:
            undo = grid.make_move(self, action[0], action[1])
            if undo is None:
                continue
            score = self._min_value(grid, alpha, beta, depth - 1)
            grid.undo_move(undo)

            if score > v:
                v = score
            if v >= beta:
                return v
            if v > alpha:
                alpha = v
        return v

    def _min_value(self, grid, alpha, beta, depth):
        if grid.winner is not None or grid.has_winner():
            return self._utility(grid)
        if grid.is_full():
            return self._utility(grid)
        if depth == 0:
            return self._heuristique(grid)

        actions = grid.get_possible_actions()
        if not actions:
            return self._heuristique(grid)

        if depth >= 3 and len(actions) > 4:
            actions = self._order_moves(grid, actions, maximizing=False)

        v = math.inf
        opponent = self._sim_opponent
        for action in actions:
            undo = grid.make_move(opponent, action[0], action[1])
            if undo is None:
                continue
            score = self._max_value(grid, alpha, beta, depth - 1)
            grid.undo_move(undo)

            if score < v:
                v = score
            if v <= alpha:
                return v
            if v < beta:
                beta = v
        return v

    def _order_moves(self, grid, actions, maximizing):
        """
        Trie les coups par évaluation rapide (1-ply) pour favoriser
        l'élagage alpha-bêta. Décroissant pour le joueur max, croissant
        pour le joueur min.
        """
        scored = []
        player = self if maximizing else self._sim_opponent
        for action in actions:
            undo = grid.make_move(player, action[0], action[1])
            if undo is None:
                continue
            s = self._heuristique(grid)
            grid.undo_move(undo)
            scored.append((s, action))
        scored.sort(key=lambda t: t[0], reverse=maximizing)
        return [a for _, a in scored]

    # ------------------------------------------------------------------
    # Évaluations
    # ------------------------------------------------------------------
    def _utility(self, grid):
        """Score d'un état terminal (ou supposé terminal)."""
        if grid.winner == self.symbol:
            return 100000
        if grid.winner == self.opp_symbol:
            return -100000
        # Match nul : on compte les mini-grilles gagnées (règle classique).
        my_count = 0
        opp_count = 0
        for loc in META_ORDER:
            w = grid.grid[loc].winner
            if w == self.symbol:
                my_count += 1
            elif w == self.opp_symbol:
                opp_count += 1
        if my_count > opp_count:
            return 50000
        if opp_count > my_count:
            return -50000
        return 0

    def _heuristique(self, grid):
        """
        Heuristique stratégique pour Ultimate Tic Tac Toe.

        Composantes :
          1. Si le jeu est gagné, score quasi terminal.
          2. Score des alignements du méta-plateau (priorité forte) :
             chaque ligne de 3 mini-grilles est scorée selon combien de
             mini-grilles « miennes » et « adverses » elle contient.
             Une mini-grille pleine sans gagnant bloque l'alignement.
          3. Score d'appropriation des mini-grilles, pondéré par la
             position (centre > coins > bords).
          4. Score interne de chaque mini-grille non terminée :
             alignements internes pondérés par l'importance positionnelle
             de la mini-grille.
          5. Bonus positionnel des cases occupées (faible mais utile).
        """
        if grid.winner == self.symbol:
            return 100000
        if grid.winner == self.opp_symbol:
            return -100000

        me = self.symbol
        opp = self.opp_symbol
        score = 0

        # 1) Vecteurs d'état
        meta_winners = []
        meta_full = []
        meta_grids = []
        for loc in META_ORDER:
            mg = grid.grid[loc]
            meta_winners.append(mg.winner)
            meta_full.append(mg.is_full() if mg.winner is None else False)
            meta_grids.append(mg)

        # 2) Alignements du méta-plateau (poids fort : c'est la condition
        #    de victoire principale).
        for (i, j, k) in LINES_3x3:
            a = meta_winners[i]
            b = meta_winners[j]
            c = meta_winners[k]
            # Si une case du méta est « finie sans gagnant », elle bloque
            # les deux camps -> ligne neutralisée.
            if (a is None and meta_full[i]) or \
               (b is None and meta_full[j]) or \
               (c is None and meta_full[k]):
                continue
            my_n = (a == me) + (b == me) + (c == me)
            op_n = (a == opp) + (b == opp) + (c == opp)
            score += _line_score(my_n, op_n) * 30  # gros multiplicateur

        # 3) Possession des mini-grilles, pondérée
        for idx, w in enumerate(meta_winners):
            if w == me:
                score += 80 * META_WEIGHTS[idx]
            elif w == opp:
                score -= 80 * META_WEIGHTS[idx]

        # 4 + 5) Évaluation interne des mini-grilles non terminées
        for idx, mg in enumerate(meta_grids):
            if meta_winners[idx] is not None:
                continue
            mw = META_WEIGHTS[idx]
            cells = mg.grid

            # Mise à plat pour indexation O(1)
            flat = (
                cells[0][0], cells[0][1], cells[0][2],
                cells[1][0], cells[1][1], cells[1][2],
                cells[2][0], cells[2][1], cells[2][2],
            )

            # Alignements internes
            local_score = 0
            for (i, j, k) in LINES_3x3:
                a = flat[i]; b = flat[j]; c = flat[k]
                my_n = (a == me) + (b == me) + (c == me)
                op_n = (a == opp) + (b == opp) + (c == opp)
                local_score += _line_score(my_n, op_n)

            # Bonus positionnel des cases occupées
            cell_bonus = 0
            for r in range(3):
                row_cells = cells[r]
                row_w = CELL_WEIGHTS[r]
                for c in range(3):
                    s = row_cells[c]
                    if s == me:
                        cell_bonus += row_w[c]
                    elif s == opp:
                        cell_bonus -= row_w[c]

            # On pondère le score local par l'importance de la mini-grille
            score += local_score * mw
            score += cell_bonus * mw

        return score

    # ------------------------------------------------------------------
    # Outils
    # ------------------------------------------------------------------
    def _is_empty_board(self, grid):
        for loc in META_ORDER:
            mg_cells = grid.grid[loc].grid
            for r in range(3):
                row = mg_cells[r]
                if row[0] != ' ' or row[1] != ' ' or row[2] != ' ':
                    return False
        return True
