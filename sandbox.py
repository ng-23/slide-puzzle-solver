'''
Script for experimentation
'''

from SlidePuzzle import SlidePuzzle
import tkinter as tk
import pprint

def tuplify_game_state(game_state:list[list]):
    '''
    Convert game state to tuple of tuples
    '''

    return tuple([tuple(row) for row in game_state])

def untuplify_game_state(game_states:tuple[tuple]):
    return list([list(row) for row in game_states])

def precompute_search_space(game_state:tuple[tuple], puzzle:SlidePuzzle, n_nodes:int|None=None):

    # maps a current game state to a dict
    # that maps a next game state to the move tuple that lead to it from current game state
    graph = {}

    # need to be careful to avoid explicitly introducing cycles into the graph
    # search algo will still need to figure out how to avoid them itself

    empty_pos = puzzle.empty_pos
    queue = [(game_state, [], empty_pos)] # tuple of current game state, moves made to reach current state, and position of empty tile
    seen_states = set([tuplify_game_state(game_state)])

    while queue:
        #print(f'Game states to check:\n{queue}')

        curr_state, moves_made, empty_pos = queue.pop(0)

        graph[tuplify_game_state(curr_state)] = dict()
        print(f'Unique state nodes in graph: {len(graph)}\n')
        print('Current game state:')
        # see https://stackoverflow.com/a/63496125/ (pretty printing the 2d matrix)
        for i in curr_state:
            print('   '.join(map(str, i)))

        if n_nodes is not None and len(graph) == n_nodes:
            # this just indicates that we only want to precompute the first n nodes
            print(f'\nComputed {n_nodes} state nodes, stopping early\n{'-'*25}')
            break

        possible_moves = puzzle.get_possible_moves(simulate=True, empty_pos=empty_pos)
        next_states = {tuplify_game_state(puzzle.make_move(*move, simulate=True, game_state=curr_state, empty_pos=empty_pos, possible_moves=possible_moves)): move for move in possible_moves}
        print(f'\nNext possible {len(next_states)} game states:\n{pprint.pformat(next_states, indent=4, sort_dicts=False)}\n')
        unseen_states = set(next_states.keys()) - seen_states
        print(f'{len(unseen_states)}/{len(next_states)} next possible game states are unseen:\n{unseen_states}')
        
        for unseen_state in unseen_states:
            move_to = next_states[unseen_state]
            graph[tuplify_game_state(curr_state)][unseen_state] = move_to

            seen_states.add(unseen_state)
            queue.append(
                (
                    untuplify_game_state(unseen_state), 
                    moves_made + [move_to],
                    next_states[unseen_state]
                    ))
        print('-'*25)
                
    # "The 8-puzzle (3x3) has 9!/2 ≈ 181,440 possible states, making complete exploration feasible" per README
    # each top-level key in our graph is a unique state, aka a node
    # so in other words our graph (dict) should have 181400 keys
    if n_nodes is None and len(graph) != 181440:
        raise Exception(f'Graph should have 181,400 unique state nodes - got {len(graph)} instead')
                
    return graph

def main(seed:int=42, debug=False, n_nodes:int|None=20):
    puzzle = SlidePuzzle(tk.Tk(), seed=seed, debug=debug)

    # get initial game state
    init_game_state = puzzle.current_state

    # ultimately goal is to represent search space as a graph
    # each node is the game state, each edge is a possible move
    # easiest to use a dict for this seach space representation
    # only issue is that lists are not hashable - but tuples are (immutable)

    # now we have enough info to start building the search space (graph)
    # i see 2 ways of doing this - precomputed and on-the-fly
    # precomputation - build a dictionary of every possible move and resulting state, then apply a search algo to it
    # on-the-fly - apply the search algo to initial state/moves, then at each iter compute the next possible moves and resulting states
    # let's start by doing precomputation, since that's probably easier (though it'll eat up more RAM)
    search_space = precompute_search_space(init_game_state, puzzle, n_nodes=n_nodes)
    print(search_space)

if __name__ == '__main__':
    seed = 123
    debug = True
    n_nodes = 100
    main(seed=seed, debug=debug, n_nodes=n_nodes)