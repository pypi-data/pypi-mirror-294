# MCTS
# we pass around the valid moves because we want to avoid recalculating more than once per game

import torch
import numpy as np
from aleph0.game import SelectionGame
from aleph0.algs.algorithm import Algorithm
from aleph0.algs.play_game import play_game
from aleph0.algs.nonlearning import Randy


class DummyNode:
    """
    empty node, defined to make root node the same as other nodes
    """
    DUMMY_MOVE = None

    def __init__(self, num_players):
        self.child_total_value = np.zeros((1, num_players))
        self.child_number_visits = np.zeros((1, 1))
        self.next_moves = [DummyNode.DUMMY_MOVE]
        self.move_idx = {DummyNode.DUMMY_MOVE: 0}
        self.dumb = True
        self.num_players = num_players


class Node:
    def __init__(self,
                 move,
                 parent,
                 terminal,
                 next_selection_moves,
                 next_special_moves,
                 num_players,
                 current_player,
                 exploration_constant=1.,
                 ):
        """
        Args:
            move: which move we got from parent
            terminal: whether node is terminal
            next_selection_moves: iterable of playable selection moves by player from the state
                ORDER MATTERS
            next_special_moves: iterable of playable special moves by player from the state
                ORDER MATTERS
            num_players: number of players
            parent: previous node
            exploration_constant: exploration constatn
        """
        self.move = move
        self.parent = parent
        self.terminal = terminal
        self.exp_constant = exploration_constant
        self.num_players = num_players
        self.current_player = current_player

        self.is_expanded = False
        self.children = dict()
        self.dumb = False  # not a dummy node
        self.next_selection_moves = list(next_selection_moves)
        self.next_special_moves = list(next_special_moves)
        self.next_moves = self.next_selection_moves + self.next_special_moves
        self.move_idx = {next_move: i for i, next_move in enumerate(self.next_moves)}

        # probability distribution to choose next childs (set when node is expanded for the first time)
        self.child_priors = None

        # running value estimate for self of taking each move
        self.child_total_value = np.zeros((len(self.next_moves), num_players))
        self.child_number_visits = np.zeros((len(self.next_moves), 1))

    @property
    def number_visits(self):
        return self.parent.child_number_visits[self.parent.move_idx[self.move]]

    @property
    def child_Q(self):
        return self.child_total_value/(1 + self.child_number_visits)

    @property
    def child_U(self):
        # Allegedly this version is used in alphazero
        return self.exp_constant*np.sqrt(self.number_visits)*(self.child_priors/(1 + self.child_number_visits))
        # standard UCT exploration term (multiplied by child priors)
        # return self.exp_constant*self.child_priors*np.sqrt(np.log(self.number_visits)/(1 + self.child_number_visits))

    @property
    def unexplored_indices(self):
        return np.where(self.child_number_visits == 0)[0]

    def pick_move(self):
        # we want to check the q values only of current player when picking move
        bestmove = self.child_Q[:, (self.current_player,)] + self.child_U
        if self.fully_expanded:
            return self.next_moves[np.argmax(bestmove)]
        else:
            # in this case, sample from the unexplored nodes
            return self.next_moves[max(self.unexplored_indices,
                                       key=lambda idx: self.child_priors[idx])]

    def get_final_policy(self):
        # return torch.nn.Softmax(-1)(torch.tensor(self.child_Q)).flatten().detach().numpy()
        # Alphazero uses child number visits because apparently this is less prone to outliers
        return (self.child_number_visits/np.sum(self.child_number_visits)).flatten()

    def get_final_values(self):
        # weighted sum of Q values
        return (self.get_final_policy().reshape((1, -1))@self.child_Q).flatten()

    def select_leaf(self, game: SelectionGame):
        """
        selects leaf of self, makes moves on game along the way
        :return: leaf, resulting game
        """
        current = self
        i = 0
        while current.is_expanded:
            best_move = current.pick_move()
            current, game, terminal = current.maybe_add_child(game=game, move=best_move)
            i += 1
            if terminal:
                break
        return current, game

    def add_dirichlet_noise(self, child_priors):
        """
        adds noise to a policy
        """
        child_priors = 0.75*child_priors + 0.25*np.random.dirichlet(
            np.zeros([len(child_priors)], dtype=np.float32) + 0.3)
        return child_priors

    @property
    def is_root(self):
        return isinstance(self.parent, DummyNode)

    @property
    def is_terminal(self):
        return self.terminal

    @property
    def fully_expanded(self):
        return np.all(self.child_number_visits != 0)

    def expand(self, child_priors):
        self.is_expanded = True
        if self.is_root:  # add dirichlet noise to child_priors in root node
            child_priors = self.add_dirichlet_noise(child_priors=child_priors)

        self.child_priors = child_priors.reshape((-1, 1))

    def maybe_add_child(self, game: SelectionGame, move):
        """
        makes move from current state,
            if move has not been seen, adds it to children
        returns resulting child and resulting game
            mutates game state
        """
        new_game = game.make_move(move)
        terminal = new_game.is_terminal()
        if move not in self.children:
            new_game: SelectionGame
            self.children[move] = Node(
                move=move,
                parent=self,
                terminal=terminal,
                next_selection_moves=list(new_game.valid_selection_moves()),
                next_special_moves=list(new_game.valid_special_moves()),
                num_players=self.num_players,
                current_player=new_game.current_player,
                exploration_constant=1.,
            )
        return self.children[move], new_game, terminal

    def inc_total_value_and_visits(self, value_estimate):
        idx = self.parent.move_idx[self.move]
        self.parent.child_number_visits[idx] += 1
        self.parent.child_total_value[idx] += value_estimate

    def backup(self, value_estimate: float):
        self.inc_total_value_and_visits(value_estimate=value_estimate)
        if not self.parent.dumb:
            self.parent.backup(value_estimate=value_estimate)


def UCT_search(game: SelectionGame, num_reads, policy_value_evaluator):
    """
    Args:
        game: game to evaluate
        num_reads: number of times to start a search
        policy_value_evaluator: (game, selection_moves, special_moves) -> (policy,value)
            moves is all possible moves at that point (if None, uses all possible moves)
            NOTE THAT THIS MUST DEPERMUTE IF NECESSARY
                must return true values as opposed to permuted values
                look at permutation_to_standard_pos, where (true_value[i]=network_output_value[perm[i]])
    Returns:
        final policy, final value, root node (if into that)
    """
    next_moves = list(game.get_all_valid_moves())
    root = Node(move=DummyNode.DUMMY_MOVE,
                parent=DummyNode(num_players=game.num_players),
                terminal=game.is_terminal(),
                next_selection_moves=list(game.valid_selection_moves()),
                next_special_moves=list(game.valid_special_moves()),
                num_players=game.num_players,
                current_player=game.current_player,
                exploration_constant=1.,
                )
    if not next_moves:
        return None, root
    for i in range(num_reads):
        leaf, leaf_game = root.select_leaf(game=game)
        if leaf.is_terminal:
            leaf.backup(value_estimate=leaf_game.get_result())
        else:
            policy, value_estimates = policy_value_evaluator(
                game=leaf_game,
                selection_moves=leaf.next_selection_moves,
                special_moves=leaf.next_special_moves,
            )
            leaf.expand(child_priors=policy)
            leaf.backup(value_estimate=value_estimates)
    return root.get_final_policy(), root.get_final_values(), root


class MCTS(Algorithm):
    """
    picks moves with a simple mcts
        would expect this does not go well
    """

    def __init__(self,
                 num_reads,
                 evaluation_alg: Algorithm = None,
                 depth=float('inf'),
                 heuristic_eval=None,
                 num_rollout_samples=1,
                 ):
        """
        Args:
            num_reads: number of times to initialize a game
            evaluation_alg: agent to use to search tree past leafs (or to cut short and evaluate leaf)
            depth: number of moves to make before terminating
            heuristic_eval: game -> values for each player
                for acting on non-terminal games
                probably should return a 'draw' of (.5,.5) or some other value estimate
            num_rollout_samples: number of times to rollout from a leaf(if doing rollouts)
        """
        super().__init__()
        if evaluation_alg is None:
            evaluation_alg = Randy()
        self.num_reads = num_reads
        self.evaluation_alg = evaluation_alg
        self.depth = depth
        self.heuristic_eval = heuristic_eval
        self.num_rollout_samples = num_rollout_samples

    def policy_value_eval_for_UCT(self,
                                  game: SelectionGame,
                                  selection_moves,
                                  special_moves,
                                  trials=1,
                                  ):
        """
        Args:
            game:
        Returns:

        """
        if selection_moves is None:
            selection_moves = list(game.valid_selection_moves())
        if special_moves is None:
            special_moves = list(game.valid_special_moves())

        policy, values = self.evaluation_alg.get_policy_value(game=game,
                                                              selection_moves=selection_moves,
                                                              special_moves=special_moves,
                                                              )

        if values is None:
            values = torch.zeros(game.num_players)
            for trial in range(trials):
                outcomes, histories = play_game(game=game,
                                                alg_list=[self.evaluation_alg for _ in range(game.num_players)],
                                                n=1,
                                                initial_moves=selection_moves + special_moves,
                                                save_histories=True,
                                                depth=self.depth,
                                                )
                outcome, history = outcomes[0], histories[0]
                if outcome is None:
                    _, _, final_game = history
                    outcome = self.heuristic_eval(final_game)
                values += torch.tensor(outcome, dtype=torch.float)
            values = values/trials
        return policy.numpy(), values.numpy()

    def get_policy_value(self, game: SelectionGame, selection_moves=None, special_moves=None):
        """
        gets the distribution of best moves from the state of game, as well as the value for each player
        requires that game is not at a terminal state
        Args:
            game: SubsetGame instance with K players
            selection_moves: list of valid moves to inspect (size N)
                if None, uses game.valid_selection_moves()
            special_moves: list of special moves to inspect
                if None, uses game.valid_special_moves()
        Returns:
            array of size N that determines the calculated probability of taking each move,
                in order of moves given, or game.get_all_valid_moves()
                concatenates the selection moves and special moves
            array of size K in game that determines each players expected payout
                or None if not calculated
        """
        policy, values, _ = UCT_search(
            game=game,
            num_reads=self.num_reads,
            policy_value_evaluator=(
                lambda game, selection_moves, special_moves:
                self.policy_value_eval_for_UCT(
                    game=game,
                    selection_moves=selection_moves,
                    special_moves=special_moves,
                    trials=self.num_rollout_samples,
                )
            ),
        )
        return torch.tensor(policy), torch.tensor(values)


if __name__ == '__main__':
    from aleph0.examples.tictactoe import Toe
    from aleph0.algs import Human

    game = Toe()
    game = game.make_move(next(game.get_all_valid_moves()))
    game = game.make_move(next(game.get_all_valid_moves()))
    game = game.make_move(next(game.get_all_valid_moves()))
    game = game.make_move(((2, 1),))
    # there is one winning move for player 0, and the rest are losing
    # MCTS should learn to only play the winning move
    print(game)
    alg = MCTS(num_reads=696)
    pol,val=alg.get_policy_value(game=game)
    print(pol,val)

    # checking symmetries
    print('checking symmetries')
    for sym_game,sym_pol in game.symmetries(pol):
        print()
        print(sym_game)
        print(sym_pol)




    print(play_game(Toe(), [Human(), alg])[0])
