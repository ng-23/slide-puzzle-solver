'''
Miscellaneous utilities
'''

def tuplify_game_state(game_state:list[list]):
    '''
    Convert game state to tuple of tuples
    '''

    return tuple([tuple(row) for row in game_state])

def untuplify_game_state(game_states:tuple[tuple]):
    '''
    Convert tuplified game state back to list of lists
    '''

    return list([list(row) for row in game_states])
