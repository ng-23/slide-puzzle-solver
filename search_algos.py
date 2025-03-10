'''
Search algorithms
'''

def precomputed_bfs(graph:dict[tuple,dict[tuple,tuple[int,int]]], goal_state:tuple[tuple]):
    '''
    Perform a breadth-first search on a precomputed search space graph

    `graph` is expected to (generally) look like so:

    {
        state0: {state1: (i,j), state2: (i,j)},
        ...
        stateN: {stateN+1: (i,j), stateN+2: (i,j)}
    }
    '''

    # see https://stackoverflow.com/questions/30362391/how-to-find-the-first-key-in-a-dictionary-python
    queue = [(next(iter(graph)), [])] # tuple of current state, moves made to reach current state

    seen_states = set([next(iter(graph))])

    while queue:
        curr_state, moves_made = queue.pop(0)

        if curr_state == goal_state:
            return moves_made, len(moves_made)
        
        unseen_states = set(graph[curr_state].keys()) - seen_states
        for unseen_state in unseen_states:
            move_to = graph[curr_state][unseen_state]

            seen_states.add(unseen_state)
            queue.append(
                (
                    unseen_state,
                    moves_made + [move_to]
                ),
            )

    return None, len(seen_states)

def precomputed_dfs(graph:dict[tuple,dict[tuple,tuple[int,int]]], goal_state:tuple[tuple]):
    '''
    Perform a depth-first search on a precomputed search space graph

    `graph` is expected to (generally) look like so:

    {
        state0: {state1: (i,j), state2: (i,j)},
        ...
        stateN: {stateN+1: (i,j), stateN+2: (i,j)}
    }
    '''

    stack = [(next(iter(graph)), [])] # tuple of current state, moves made to reach current state

    seen_states = set([next(iter(graph))])

    while stack:
        curr_state, moves_made = stack.pop(-1) # -1 is alias for last index

        if curr_state == goal_state:
            return moves_made, len(moves_made)
        
        unseen_states = set(graph[curr_state].keys()) - seen_states
        for unseen_state in unseen_states:
            move_to = graph[curr_state][unseen_state]

            seen_states.add(unseen_state)
            stack.append(
                (
                    unseen_state,
                    moves_made + [move_to]
                ),
            )

    return None, len(seen_states)

def precomputed_gbfs(graph:dict[tuple,dict[tuple,tuple[int,int]]], goal_state:tuple[tuple]):
    '''
    Perform a greedy breadth-first search on a precomputed search space graph (with edge costs)

    `graph` is expected to (generally) look like so:

    ```
    {
        state0: {state1: (i,j,cost1), state2: (i,j,cost2)},
        ...
        stateN: {stateN+1: (i,j,costN+1), stateN+2: (i,j,costN+2)}
    }
    ```
    
    General cost function: f(n) = h(n)
    - n is a node, which in this case is a state
    - f(n) is the cost function
    - h(n) is the heuristic function, which generally estimates the "cost" of going from the current state to the goal state
    '''
    pass