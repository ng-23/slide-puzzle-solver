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

def precomputed_gbfs(graph:dict[tuple,dict[tuple,tuple[int,int,int]]], goal_state:tuple[tuple]):
    '''
    Perform a greedy best-first search on a precomputed search space graph (with edge costs)

    `graph` is expected to (generally) look like so:

    ```
    {
        state0: {state1: (i,j,heuristicCost1), state2: (i,j,heuristicCost2)},
        ...
        stateN: {stateN+1: (i,j,heuristicCostN+1), stateN+2: (i,j,heuristicCostN+2)}
    }
    ```
    
    General cost function: f(n) = h(n)
    - n is a node, which in this case is a state
    - f(n) is the cost function
    - h(n) is the heuristic function, which generally estimates the "cost" of going from the current state to the goal state

    See https://en.wikipedia.org/wiki/Best-first_search

    See https://www.codecademy.com/resources/docs/ai/search-algorithms/greedy-best-first-search

    See https://stackoverflow.com/questions/8374308/is-the-greedy-best-first-search-algorithm-different-from-the-best-first-search-a
    '''

    moves_made, reached_goal = [], False

    pque = PriorityQueue()
    pque.put((
        0,
        [],
        next(iter(graph))
    )) # tuple of cost to reach current state given by f(n), moves made to reach current state, current state

    while not pque.empty():
        curr_cost, moves_made, curr_state = pque.get()

        if curr_state == goal_state:
            reached_goal = True
            break
        
        next_states = graph[curr_state].keys()
        
        for next_state in next_states:
            data = graph[curr_state][next_state]
            heuristic_cost= data[-1] # h(n)
            
            pque.put(
                (
                    heuristic_cost, # f(n) = h(n)
                    moves_made + [data[:-1]],
                    next_state,
                )
            )

    return moves_made, len(moves_made), reached_goal

def precomputed_Astar(graph:dict[tuple,dict[tuple,tuple[int,int,int]]], goal_state:tuple[tuple]):
    '''
    Perform am A* search on a precomputed search space graph (with edge costs)

    `graph` is expected to (generally) look like so:

    ```
    {
        state0: {state1: (i,j,heuristicCost1), state2: (i,j,heuristicCost2)},
        ...
        stateN: {stateN+1: (i,j,heuristicCostN+1), stateN+2: (i,j,heuristicCostN+2)}
    }
    ```
    
    General cost function: f(n) = g(n) + h(n)
    - n is a node, which in this case is a state
    - f(n) is the cost function
    - g(n) is the cost to reach the next node in the current path
    - h(n) is the heuristic function, which generally estimates the "cost" of going from the current state to the goal state'
    '''

    moves_made, reached_goal = [], False

    pque = PriorityQueue()
    pque.put((
        0,
        [],
        next(iter(graph))
    )) # tuple of cost to reach current state given by f(n), moves made to reach current state, current state

    while not pque.empty():
        curr_cost, moves_made, curr_state = pque.get()

        if curr_state == goal_state:
            reached_goal = True
            break

        next_states = graph[curr_state].keys()
        
        for next_state in next_states:
            data = graph[curr_state][next_state]
            path_cost, heuristic_cost = len(moves_made)+1, data[-1] # g(n) and h(n)

            pque.put(
                (
                    heuristic_cost + path_cost, # f(n) = g(n) + h(n)
                    moves_made + [data[:-1]],
                    next_state,
                )
            )

    return moves_made, len(moves_made), reached_goal