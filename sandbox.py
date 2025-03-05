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

def untuplify_game_state(game_states:tuple[tuple]):
    return list([list(row) for row in game_states])

def precompute_graph(game_state:tuple[tuple], puzzle:SlidePuzzle):

    # maps a current game state to a dict
    # that maps a next game state to the move tuple that lead to it from current game state
    graph = {}

    # need to be careful to avoid explicitly introducing cycles into the graph
    # search algo will still need to figure out how to avoid them itself

    empty_pos = puzzle.empty_pos
    queue = [(game_state, [], empty_pos)] # tuple of current game state, moves made to reach current state, and position of empty tile
    seen_states = set([tuplify_game_state(game_state)])

    while queue:
        print(f'Game states to check:\n{queue}')

        curr_state, moves_made, empty_pos = queue.pop(0)

        graph[tuplify_game_state(curr_state)] = {'moves_made':moves_made, 'empty_pos':empty_pos}
        print(f'Unique nodes in graph: {len(graph)}')

        next_states = {tuplify_game_state(puzzle.make_move(*move, simulate=True, game_state=curr_state, empty_pos=empty_pos)): move for move in puzzle.get_possible_moves(simulate=True, empty_pos=empty_pos)}
        print(f'Next possible game states:\n{next_states}')

        for next_state in next_states:
            if next_state not in seen_states:
                seen_states.add(next_state)
                queue.append(
                    (
                        untuplify_game_state(next_state), 
                        moves_made + [next_states[next_state]],
                        next_states[next_state]
                        ))
                
        if len(graph) == 3:
            break

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

    # now we have enough info to start building the search space (graph)
    # i see 2 ways of doing this - precomputed and on-the-fly (not sure if OTF would work yet though...)
    # precomputation - build a dictionary of every possible move and resulting state, then apply a search algo to it
    # on-the-fly - apply the search algo to initial state/moves, then at each iter compute the next possible moves and resulting states
    # let's start by doing precomputation, since that's probably easier (though it'll eat up more RAM)
    search_space = precompute_graph(game_state, puzzle)
    print(search_space)

if __name__ == '__main__':
    main()