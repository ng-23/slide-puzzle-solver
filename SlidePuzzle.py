import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random
import copy
import utils
from typing import Literal
import pprint
import search_algos as sa

class SlidePuzzle:
    def __init__(
            self, 
            root:tk.Tk, 
            solve_method:Literal['pc_bfs']='pc_bfs', 
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
        self.solve_method = solve_method
        self.solve_config = solve_config
        self.rand = random.Random(self.seed)

        # UI stuff
        self.size = 3  # 3x3 grid
        self.buttons = []
        self.tile_size = 135  # Size of each tile in pixels
        self.image_tiles = []        
        
        # Game state
        self.current_state = []
        self.empty_pos = None
        self.num_moves = 0
        self.goal_state = utils.tuplify_game_state(self.calc_goal_state() if goal_state is None else goal_state)
        
        # Create UI elements
        self.create_menu()

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
        self.shuffle_board()
        
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
            
            # Create game board
            self.create_board()
            self.shuffle_btn.config(state=tk.NORMAL)
            
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
                            command=lambda x=i, y=j: self.make_move(x, y))
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)
            
        # Initialize game state
        self.current_state = [[i * self.size + j 
                            for j in range(self.size)]
                            for i in range(self.size)]
        
        # Set the empty position to the bottom right
        self.empty_pos = (self.size - 1, self.size - 1)
            
    def shuffle_board(self):
        # Perform random moves
        for _ in range(100):
            possible_moves = self.get_possible_moves()
            i, j = self.rand.choice(possible_moves)
            self.swap_tiles(i, j)
        self.num_moves = 0
        # Update display
        self.update_display()
        
    def get_possible_moves(self, simulate=False, empty_pos=()):
        moves = []

        if simulate:
            i, j = empty_pos
        else:
            i, j = self.empty_pos
            
        # Check all adjacent positions
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < self.size and 0 <= new_j < self.size:
                moves.append((new_i, new_j))
    
        return moves
        
    def make_move(self, i, j, simulate=False, game_state=None, empty_pos=(), possible_moves:list[tuple[int,int]]=[]) -> None|list[list[int]]:
        # simulate making the move, but don't actually change the board
        if simulate:
            if game_state is None:
                # no state provided which is necessary for simulation to work properly
                return None
            
            if len(empty_pos) < 2:
                # need to know empty position for simulation to work properly
                return None
            
            if len(possible_moves) == 0:
                # possible moves not already supplied so calculate them
                possible_moves = self.get_possible_moves(simulate=True, empty_pos=empty_pos)
                
            # assumes possible moves provided (or calculated) are indeed valid
            if (i,j) not in possible_moves:
                return None # invalid move, no valid board
            
            # make a copy of the game state - otherwise our modifications will be done in-place
            # which will mess up subsequent move simulations
            curr_state = copy.deepcopy(game_state)
                        
            # move must be valid
            # just swap the empty tile with the tile at the i,j position
            empty_i, empty_j = empty_pos
            empty_tile = curr_state[empty_i][empty_j] # actual empty tile number
            swap_tile = curr_state[i][j] # actual soon-to-be-swapped tile number
            curr_state[empty_i][empty_j] = swap_tile
            curr_state[i][j] = empty_tile

            return curr_state

        # not a simulation - carry out the move and update the board
        # Check if the clicked tile is adjacent to empty space
        if (i, j) in self.get_possible_moves():
            self.num_moves += 1
            self.swap_tiles(i, j)
            self.update_display()
            # Check if puzzle is solved
            if self.check_win():
                messagebox.showinfo(
                    "Congratulations!", "You solved the puzzle in " +str(self.num_moves) + " moves!"
                    )
                
    def swap_tiles(self, i, j):
        # Swap values in current_state
        empty_i, empty_j = self.empty_pos
        self.current_state[empty_i][empty_j] = self.current_state[i][j]
        self.current_state[i][j] = self.size * self.size - 1
        self.empty_pos = (i, j)
        
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
            print(f'Possible moves:\n{self.get_possible_moves()}')
            print('-'*50)
   
    def check_win(self):
        '''
        Check if current game state equals goal state
        '''

        return self.goal_state == utils.tuplify_game_state(self.current_state)
    
    def precompute_search_space(self, init_game_state:tuple[tuple], init_empty_pos:tuple[int,int], n_nodes:int|None=None):
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
        seen_states = set([utils.tuplify_game_state(init_game_state)])

        while queue:
            curr_state, moves_made, empty_pos = queue.pop(0)

            graph[utils.tuplify_game_state(curr_state)] = dict()

            if n_nodes is not None and len(graph) == n_nodes:
                # this just indicates that we only want to precompute the first n nodes
                break

            possible_moves = self.get_possible_moves(simulate=True, empty_pos=empty_pos)
            next_states = {utils.tuplify_game_state(self.make_move(*move, simulate=True, game_state=curr_state, empty_pos=empty_pos, possible_moves=possible_moves)): move for move in possible_moves}
            unseen_states = set(next_states.keys()) - seen_states

            for unseen_state in unseen_states:
                move_to = next_states[unseen_state]
                graph[utils.tuplify_game_state(curr_state)][unseen_state] = move_to

                seen_states.add(unseen_state)
                queue.append(
                    (
                        utils.untuplify_game_state(unseen_state), 
                        moves_made + [move_to],
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

        if self.solve_method == 'pc_bfs':
            moves_made, num_moves = self._solve_pc_bfs()
        else:
            raise ValueError(f'Unknown/unimplemented solve method {self.solve_method}')
        
        print(f'Correct sequence of {num_moves} moves:\n{moves_made}')

        for move in moves_made:
            self.make_move(*move)

    def _solve_pc_bfs(self) -> list[tuple[int,int]]:
        print('Solving game using precomputed BFS method...')

        search_space = self.precompute_search_space(self.current_state, self.empty_pos, **self.solve_config)
        moves_made, num_moves = sa.precomputed_bfs(search_space, self.goal_state)

        return moves_made, num_moves

if __name__ == "__main__":
    # for testing purposes only
    seed = 123
    debug = True
    solve_method = 'pc_bfs'
    solve_config = {'n_nodes':None}
    # note - w/ seed 123 and 100 nodes, this is the 100th state (node)
    goal_state = [
        [0,1,4],
        [5,3,2],
        [7,8,6],
        ]
    
    root = tk.Tk()
    game = SlidePuzzle(root, solve_method=solve_method, solve_config=solve_config, goal_state=None, seed=seed, debug=debug)
    root.mainloop()
