'''
Search algorithms
'''

from queue import PriorityQueue
from typing import Literal

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

    moves_made, reached_goal = [], False

    while queue:
        curr_state, moves_made = queue.pop(0)

        if curr_state == goal_state:
            reached_goal = True
            break
        
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

    return moves_made, len(moves_made), reached_goal

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

    moves_made, reached_goal = [], False

    while stack:
        curr_state, moves_made = stack.pop(-1) # -1 is alias for last index

        if curr_state == goal_state:
            reached_goal = True
            break
        
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

    return moves_made, len(moves_made), reached_goal

def precomputed_gbfs(graph:dict[tuple,dict[tuple,tuple[int,int,int]]], goal_state:tuple[tuple], cost_direction:Literal['min','max']='min'):
    '''
    Perform a greedy best-first search on a precomputed search space graph (with edge costs)

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

    See https://www.codecademy.com/resources/docs/ai/search-algorithms/greedy-best-first-search
    '''

    cost_direction = 'min'
    if cost_direction != 'min' and cost_direction != 'max':
        raise ValueError(f'Unknown/unimplemented cost direction {cost_direction}')

    moves_made, reached_goal = [], False

    pque = PriorityQueue()
    pque.put((
        0,
        [],
        next(iter(graph))
    )) # tuple of cost to reach current state, moves made to reach current state, current state

    while not pque.empty():
        curr_cost, moves_made, curr_state = pque.get()

        if curr_state == goal_state:
            reached_goal = True
            break
        
        next_states = graph[curr_state].keys()
        best_next_stack, best_next_cost = [], float('inf') if cost_direction == 'min' else float('-inf')
        for next_state in next_states:
            next_cost = graph[curr_state][next_state][-1]

            found_better = False
            if cost_direction == 'min':
                if next_cost < best_next_cost:
                    best_next_cost = next_cost
                    found_better = True
            else:
                if next_cost > best_next_cost:
                    best_next_cost = next_cost
                    found_better = True
            
            if found_better:
                best_next_stack.append(next_state)

        if best_next_stack:
            best_next_state = best_next_stack.pop(0)
            pque.put(
                (
                    best_next_cost,
                    moves_made + [graph[curr_state][best_next_state][:-1]],
                    best_next_state,
                )
            )

    return moves_made, len(moves_made), reached_goal