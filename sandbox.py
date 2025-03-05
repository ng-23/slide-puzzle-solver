'''
Script for experimentation
'''

from SlidePuzzle import SlidePuzzle
import tkinter as tk

def tuplify_game_state(game_state:list[list]):
    '''
    Convert game state to tuple of tuples
    '''

    return tuple([tuple(row) for row in game_state])

def precompute_graph(game_state:tuple[tuple], moves:list[tuple[int,int]], puzzle:SlidePuzzle):

    # maps a current game state to a dict
    # that maps a next game state to the move tuple that lead to it from current game state
    graph = {}

    # need to be careful to avoid explicitly introducing cycles into the graph
    # search algo will still need to figure out how to avoid them itself

    return graph

def main():
    puzzle = SlidePuzzle(tk.Tk(), debug=False)

    # get initial game state
    game_state = puzzle.current_state
    print(f'Initial game state:\n{game_state}')

    # ultimately goal is to represent search space as a graph
    # each node is the game state, each edge is a possible move
    # easiest to use a dict for this seach space representation
    # only issue is that lists are not hashable - but tuples are (immutable)
    game_state = tuplify_game_state(game_state)
    print(f'Tuplified initial game state:\n{game_state}')

    # get the initial possible moves
    moves = puzzle.get_possible_moves()
    print(f'Initial possible moves:\n{moves}')

    # now we have enough info to start building the search space (graph)
    # i see 2 ways of doing this - precomputed and on-the-fly (not sure if OTF would work yet though...)
    # precomputation - build a dictionary of every possible move and resulting state, then apply a search algo to it
    # on-the-fly - apply the search algo to initial state/moves, then at each iter compute the next possible moves and resulting states
    # let's start by doing precomputation, since that's probably easier (though it'll eat up more RAM)
    search_space = precompute_graph(game_state, moves, puzzle)

if __name__ == '__main__':
    main()