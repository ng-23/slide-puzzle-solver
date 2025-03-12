import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import copy
import utils
from typing import Literal
import search_algos as sa
import time

class SlidePuzzle:
    def __init__(
            self, 
            root:tk.Tk, 
            solve_algo:Literal['pc_bfs','pc_dfs']='pc_bfs', 
            solve_config:dict={}, 
            goal_state:list[list[int]]|None=None, 
            seed:int=42, 
            debug:bool=False
            ):
        # general properties
        self.root = root
        self.root.title("Image Slide Puzzle")
        self.seed = seed
        self.debug = debug
        self.solve_algo = solve_algo
        self.solve_config = solve_config
        self.rand = random.Random(self.seed)

        # UI stuff
        self.size = 3  # 3x3 grid
        self.buttons = []
        self.tile_size = 135  # Size of each tile in pixels
        self.image_tiles = []      
        self.disable_shuffle = True if goal_state is not None else False  
        
        # Game state
        self.current_state = []
        self.empty_pos = None
        self.num_moves = 0
        self.goal_state = utils.tuplify_2dmatrix(self.calc_goal_state() if goal_state is None else goal_state)
        
        # Create UI elements
        self.create_menu()
        self.create_board()
        self.shuffle_board()

    def calc_goal_state(self):
        state = []

        for r in range(self.size):
            row = []
            for c in range(self.size):
                expected = r * self.size + c
                row.append(expected)
            state.append(row)
                    
        return state

    def create_menu(self):
        # Create a frame for the menu
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=10)
        
        # Add solve game button
        load_btn = tk.Button(menu_frame, text="Solve Game", 
                            command=self.solve_game)
        load_btn.pack(side=tk.LEFT, padx=5)

        # Add shuffle button (initially disabled)
        self.shuffle_btn = tk.Button(menu_frame, text="Shuffle",
                                   command=self.shuffle_board,
                                   state=tk.DISABLED)
        self.shuffle_btn.pack(side=tk.LEFT, padx=5)
        self.load_image()
        
    def load_image(self):
        # Open file dialog to choose an image
        file_path = '/home/noahg/COSC405/assignment2/slide-puzzle-solver-assignment-ng-23/img.jpg'
        
        if file_path:
            # Load and resize image
            image = Image.open(file_path)
            image = image.resize((self.tile_size * self.size, 
                                self.tile_size * self.size))
            
            # Split image into tiles
            self.image_tiles = []
            for i in range(self.size):
                for j in range(self.size):
                    # Calculate tile coordinates
                    left = j * self.tile_size
                    top = i * self.tile_size
                    right = left + self.tile_size
                    bottom = top + self.tile_size
                
                    # Crop tile from image
                    tile = image.crop((left, top, right, bottom))
                    # make it black if it is the empty tile
                    if i == self.size - 1 and j == self.size - 1:
                        tile = Image.new('RGB', tile.size, color='black')
                    photo = ImageTk.PhotoImage(tile)
                    self.image_tiles.append(photo)
            
    def create_board(self):
        # Create or clear game frame
        if hasattr(self, 'game_frame'):
            self.game_frame.destroy()
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(pady=10)
        
        # Create buttons for each cell
        self.buttons = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                number = i * self.size + j
                # Create button with command for ALL tiles
                btn = tk.Button(self.game_frame,
                            image=self.image_tiles[number],
                            command=lambda x=i, y=j: self.make_move((x,y), self.current_state, self.empty_pos, simulate=False))
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)
            
        # Initialize game state
        self.current_state = [[i * self.size + j 
                            for j in range(self.size)]
                            for i in range(self.size)]
        
        # Set the empty position to the bottom right
        self.empty_pos = (self.size - 1, self.size - 1)

        self.shuffle_btn.config(state=tk.NORMAL if not self.disable_shuffle else tk.DISABLED)

    def update_display(self):
        # Update button images based on current_state
        for i in range(self.size):
            for j in range(self.size):
                value = self.current_state[i][j]
                if value == self.size * self.size - 1:
                    # This is the empty tile
                    self.buttons[i][j].config(image=self.image_tiles[value])
                else:
                    self.buttons[i][j].config(image=self.image_tiles[value])
        if self.debug:
            print(f'Total moves: {self.num_moves}')
            print(f'Current game state:\n{self.current_state}')
            print(f'Empty position:\n{self.empty_pos}')
            print(f'Possible moves:\n{self.get_possible_moves(self.empty_pos)}')
            print('-'*50)
            
    def shuffle_board(self):
        # Perform random moves
        for _ in range(100):
            possible_moves = self.get_possible_moves(self.empty_pos)
            i, j = self.rand.choice(possible_moves)
            self.swap_tiles((i,j), self.current_state, self.empty_pos, simulate=False)
        self.num_moves = 0
        # Update display
        self.update_display()
        
    def get_possible_moves(self, empty_pos):
        moves = []

        i, j = empty_pos
            
        # Check all adjacent positions
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < self.size and 0 <= new_j < self.size:
                moves.append((new_i, new_j))
    
        return moves
        
    def make_move(self, new_pos, game_state, empty_pos, possible_moves=[], simulate=False):
        i, j = new_pos
        possible_moves = possible_moves if possible_moves else self.get_possible_moves(empty_pos)
        # make a copy of the game state - otherwise our modifications will be done in-place
        # which will mess up subsequent moves
        curr_state = copy.deepcopy(game_state)
        
        if (i,j) in possible_moves:
            self.swap_tiles((i,j), curr_state, empty_pos, simulate=simulate)

            if not simulate:
                self.current_state = curr_state
                self.empty_pos = (i,j)
                self.num_moves += 1

                self.update_display()
                if self.check_solved():
                    messagebox.showinfo(
                        "Congratulations!", "You solved the puzzle in " + str(self.num_moves) + " moves!"
                        )
                    
        return curr_state
                
    def swap_tiles(self, swap_pos, game_state, empty_pos, simulate=False):
        empty_i, empty_j = empty_pos
        swap_i, swap_j = swap_pos
        empty_val, swap_val = game_state[empty_i][empty_j], game_state[swap_i][swap_j]

        game_state[empty_i][empty_j] = swap_val
        game_state[swap_i][swap_j] = empty_val

        if not simulate:
            self.empty_pos = (swap_i,swap_j)

        return (swap_i,swap_j) # returns the new empty tile position
   
    def check_solved(self):
        '''
        Check if current game state equals goal state
        '''

        return self.goal_state == utils.tuplify_2dmatrix(self.current_state)
    
    def calc_total_manhattan_dist(self, game_state, goal_state, goal_vals_map={}):
        '''
        Calculate the total Manhattan Distance between tiles in current `game_state` and final `goal_state`
        '''

        dist = 0

        if not goal_vals_map:
            # create dict mapping tile vals in goal state to their row,column positions for faster lookups
            goal_vals_map = utils.get_vals_map(goal_state, self.size)
            
        for r in range(self.size):
            for c in range(self.size):
                curr_val = game_state[r][c]
                goal_val_pos = goal_vals_map[curr_val]

                dist += utils.calc_2dmanhattan_dist((r,c), goal_val_pos)

        return dist
    
    def precompute_search_space(self, init_game_state:tuple[tuple], init_empty_pos:tuple[int,int], goal_state, cost_func:str='', n_nodes:int|None=None):
        '''
        Computes a graph representing every possible unique game state and the moves to reach it
        '''

        # maps a current game state to a dict
        # that maps a next game state to the move tuple that lead to it from current game state
        graph = {}

        # need to be careful to avoid explicitly introducing cycles into the graph
        # search algo will still need to figure out how to avoid them itself

        empty_pos = init_empty_pos
        queue = [(init_game_state, [], empty_pos)] # tuple of current game state, moves made to reach current state, and position of empty tile
        seen_states = set([utils.tuplify_2dmatrix(init_game_state)])

        if cost_func == 'manhattan_dist':
            goal_vals_map = utils.get_vals_map(goal_state, self.size)

        while queue:
            curr_state, moves_made, empty_pos = queue.pop(0)

            graph[utils.tuplify_2dmatrix(curr_state)] = dict()

            if n_nodes is not None and len(graph) == n_nodes:
                # this just indicates that we only want to precompute the first n nodes
                break

            possible_moves = self.get_possible_moves(empty_pos=empty_pos)
            next_states = {utils.tuplify_2dmatrix(self.make_move(move, curr_state, empty_pos, possible_moves=possible_moves, simulate=True)): move for move in possible_moves}
            unseen_states = set(next_states.keys()) - seen_states

            for unseen_state in unseen_states:
                state_data = next_states[unseen_state]

                if cost_func == 'manhattan_dist':
                    state_data = state_data + tuple([self.calc_total_manhattan_dist(unseen_state, goal_state, goal_vals_map=goal_vals_map)])

                graph[utils.tuplify_2dmatrix(curr_state)][unseen_state] = state_data

                seen_states.add(unseen_state)
                queue.append(
                    (
                        utils.listify_2dmatrix(unseen_state), 
                        moves_made + [next_states[unseen_state]],
                        next_states[unseen_state]
                    )
                )

        # "The 8-puzzle (3x3) has 9!/2 ≈ 181,440 possible states, making complete exploration feasible" per README
        # each top-level key in our graph is a unique state, aka a node
        # so in other words our graph (dict) should have 181400 keys
        if n_nodes is None and len(graph) != 181440:
            raise Exception(f'Graph should have 181,400 unique state nodes - got {len(graph)} instead')
                    
        return graph
    
    def solve_game(self):
        moves_made, num_moves = [], 0

        if self.debug:
            print(f'Solve algorithm: {self.solve_algo}')

        if self.solve_algo == 'pc_bfs':
            moves_made, num_moves, reached_goal, solve_time = self.solve_pc_bfs()
        elif self.solve_algo == 'pc_dfs':
            moves_made, num_moves, reached_goal, solve_time = self.solve_pc_dfs()
        elif self.solve_algo == 'pc_gbfs':
            moves_made, num_moves, reached_goal,solve_time = self.solve_pc_gbfs()
        else:
            raise ValueError(f'Unknown/unimplemented solve algorithm {self.solve_algo}')
        
        if self.debug:
            print(f'Reached goal state: {reached_goal}')
            print(f'Total time: {solve_time} seconds')
            print(f'Made {num_moves} moves:\n{moves_made}')
            print('-'*50)

        if reached_goal:
            for move in moves_made:
                self.make_move(move, self.current_state, self.empty_pos, simulate=False)
            
    def solve_pc_bfs(self):
        '''
        Solve the puzzle using a BFS over a precomputed search space graph
        '''

        start = time.time()
        
        search_space = self.precompute_search_space(self.current_state, self.empty_pos, self.goal_state, **self.solve_config)
        
        return *sa.precomputed_bfs(search_space, self.goal_state), time.time()-start
 
    def solve_pc_dfs(self):
        '''
        Solve the puzzle using a DFS over a precomputed search space graph
        '''

        start = time.time()
        
        search_space = self.precompute_search_space(self.current_state, self.empty_pos, self.goal_state, **self.solve_config)
        
        return *sa.precomputed_dfs(search_space, self.goal_state), time.time()-start
    
    def solve_pc_gbfs(self):
        '''
        Solve the puzzle using a GBFS over a precomputed search space graph w/ cost
        '''

        if 'cost_func' not in self.solve_config:
            self.solve_config['cost_func'] = 'manhattan_dist'

        start = time.time()
        
        search_space = self.precompute_search_space(self.current_state, self.empty_pos, self.goal_state, **self.solve_config)
        
        return *sa.precomputed_gbfs(search_space, self.goal_state), time.time()-start

if __name__ == "__main__":
    # for testing purposes only
    seed = 123
    debug = True
    solve_method = 'pc_bfs'
    solve_config = {'n_nodes':None}
    # TODO: this doesn't work, sometimes crashes if n_nodes is set too low
    goal_state = [
        [0,1,4],
        [3,6,8],
        [5,2,7],
        ]
    
    root = tk.Tk()
    game = SlidePuzzle(root, solve_algo=solve_method, solve_config=solve_config, goal_state=None, seed=seed, debug=debug)
    root.mainloop()