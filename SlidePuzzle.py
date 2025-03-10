import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import copy
import utils
from typing import Literal
import search_algos as sa
import pprint

class SlidePuzzle:
    def __init__(
            self, 
            root:tk.Tk, 
            solve_algo:Literal['pc_bfs','pc_dfs']='pc_bfs', 
            solve_config:dict={}, 
            goal_state:utils.UniqueGrid|None=None, 
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
        
        # Game state
        self.current_state = utils.UniqueGrid(size=self.size)
        self.empty_pos = None
        self.num_moves = 0
        self.goal_state = utils.UniqueGrid(size=3).get_space(tuplify=True) if goal_state is None else goal_state.get_space(tuplify=True)
        
        # Create UI elements
        self.create_menu()

    def create_menu(self):
        # Create a frame for the menu
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=10)
        
        # Add solve game button
        load_btn = tk.Button(
            menu_frame, 
            text="Solve Game", 
            command=self.solve_game,
            )
        load_btn.pack(side=tk.LEFT, padx=5)

        # Add shuffle button (initially disabled)
        self.shuffle_btn = tk.Button(
            menu_frame, 
            text="Shuffle",
            command=self.shuffle_board,
            state=tk.DISABLED,
            )
        self.shuffle_btn.pack(side=tk.LEFT, padx=5)

        self.load_image()

        self.shuffle_board()
        
    def load_image(self):
        # Open file dialog to choose an image
        file_path = '/home/noahg/COSC405/assignment2/slide-puzzle-solver-assignment-ng-23/img.jpg'
        
        if file_path:
            # Load and resize image
            image = Image.open(file_path)
            image = image.resize(
                (self.tile_size * self.size, self.tile_size * self.size),
                )
            
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
                btn = tk.Button(
                    self.game_frame,
                    image=self.image_tiles[number],
                    command=lambda x=i, y=j: self.make_move(x, y, self.current_state, self.empty_pos, simulate=False),
                    )
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)
        
        # Set the empty position to the bottom right
        self.empty_pos = (self.size - 1, self.size - 1)
            
    def shuffle_board(self):
        # Perform random moves
        for _ in range(100):
            possible_moves = self.get_possible_moves(self.empty_pos)
            i, j = self.rand.choice(possible_moves)
            self.empty_pos = self.swap_tiles(i, j, self.current_state)
        self.num_moves = 0

        # Update display
        self.update_display()
        
    def get_possible_moves(self, empty_pos:tuple[int,int]):
        moves = []

        i, j = empty_pos
            
        # Check all adjacent positions
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < self.size and 0 <= new_j < self.size:
                moves.append((new_i, new_j))
    
        return moves
        
    def make_move(self, i:int, j:int, game_state:utils.UniqueGrid, empty_pos:tuple[int,int], possible_moves:list[tuple[int,int]]=[], simulate=False):
        possible_moves = possible_moves if possible_moves else self.get_possible_moves(empty_pos)
        if (i,j) in possible_moves:
            temp_state = copy.deepcopy(game_state)
            empty_pos = self.swap_tiles(i, j, temp_state)

            if not simulate:
                self.num_moves += 1
                self.current_state = temp_state
                self.empty_pos = empty_pos
                self.update_display()
                # Check if puzzle is solved
                if self.check_win():
                    messagebox.showinfo(
                        "Congratulations!", "You solved the puzzle in " + str(self.num_moves) + " moves!"
                        )
                    
            return temp_state
                        
    def swap_tiles(self, i, j, game_state:utils.UniqueGrid):
        game_state.swap(self.empty_pos, (i,j))
        
        return (i,j)
        
    def update_display(self):
        # Update button images based on current_state
        for i in range(self.size):
            for j in range(self.size):
                value = self.current_state.get_val((i,j))
                if value == self.current_state.get_val(self.empty_pos):
                    # This is the empty tile
                    self.buttons[i][j].config(image=self.image_tiles[value])
                else:
                    self.buttons[i][j].config(image=self.image_tiles[value])
        if self.debug:
            print(f'Total moves: {self.num_moves}')
            print(f'Current game state:\n{self.current_state}')
            print(f'Possible moves:\n{self.get_possible_moves(self.empty_pos)}')
            print('-'*50)
   
    def check_win(self):
        '''
        Check if current game state equals goal state
        '''

        return self.goal_state == self.current_state.get_space(tuplify=True)
    
    def precompute_search_space(self, init_game_state:utils.UniqueGrid, init_empty_pos:tuple[int,int], n_nodes:int|None=None):
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
        seen_states = set([init_game_state.get_space(tuplify=True)])

        while queue:
            curr_state, moves_made, empty_pos = queue.pop(0)

            graph[curr_state.get_space(tuplify=True)] = dict()
            if self.debug:
                print(f'Unique state nodes in graph: {len(graph)}\n')
                print(f'Current game state:\n{curr_state}')

            if n_nodes is not None and len(graph) == n_nodes:
                # this just indicates that we only want to precompute the first n nodes
                if self.debug:
                    print(f'Computed {n_nodes} state nodes, stopping early\n{'-'*25}')
                break

            possible_moves = self.get_possible_moves(empty_pos)
            next_states = {self.make_move(*move, curr_state, empty_pos, possible_moves=possible_moves, simulate=True): move for move in possible_moves}
            unseen_states = set(next_states.keys()) - seen_states
            if self.debug:
                print(f'Next possible {len(next_states)} game states:')
                for i,next_state in enumerate(next_states.keys()):
                    print(f'{i}:\n' + str(next_state))
                
                print(f'{len(unseen_states)}/{len(next_states)} next possible game states are unseen:')
                for i,next_state in enumerate(next_states.keys()):
                    print(f'{i}:\n' + str(next_state))
            
            for unseen_state in unseen_states:
                move_to = next_states[unseen_state]
                graph[curr_state.get_space(tuplify=True)][unseen_state.get_space(tuplify=True)] = move_to

                seen_states.add(unseen_state)
                queue.append(
                    (
                        unseen_state, 
                        moves_made + [move_to],
                        next_states[unseen_state]
                    )
                )
            if self.debug:
                print('-'*25)

        # "The 8-puzzle (3x3) has 9!/2 ≈ 181,440 possible states, making complete exploration feasible" per README
        # each top-level key in our graph is a unique state, aka a node
        # so in other words our graph (dict) should have 181400 keys
        if n_nodes is None and len(graph) != 181440:
            raise Exception(f'Graph should have 181,400 unique state nodes - got {len(graph)} instead')
                    
        return graph
    
    def solve_game(self):
        moves_made, num_moves = [], 0

        if self.debug:
            print(f'Solving game using {self.solve_algo} algorithm...')

        if self.solve_algo == 'pc_bfs':
            moves_made, num_moves = self.solve_pc_bfs()
        elif self.solve_algo == 'pc_dfs':
            moves_made, num_moves = self.solve_pc_dfs()
        else:
            raise ValueError(f'Unknown/unimplemented solve algorithm {self.solve_algo}')
        
        print(f'Correct sequence of {num_moves} moves:\n{moves_made}')

        for move in moves_made:
            self.make_move(*move, self.current_state, self.empty_pos, simulate=False)
            
    def solve_pc_bfs(self):
        '''
        Solve the puzzle using a Breadth-First Search over a precomputed search space graph
        '''

        search_space = self.precompute_search_space(copy.deepcopy(self.current_state), self.empty_pos, **self.solve_config)
        moves_made, num_moves = sa.precomputed_bfs(search_space, self.goal_state)

        return moves_made, num_moves
    
    def solve_pc_dfs(self):
        '''
        Solve the puzzle using a Depth-First Search over a precomputed search space graph
        '''

        search_space = self.precompute_search_space(copy.deepcopy(self.current_state), self.empty_pos, **self.solve_config)
        moves_made, num_moves = sa.precomputed_dfs(search_space, self.goal_state)

        return moves_made, num_moves

if __name__ == "__main__":
    # for testing purposes only
    seed = 123
    debug = False
    solve_method = 'pc_bfs'
    solve_config = {'n_nodes':None}
    
    root = tk.Tk()
    game = SlidePuzzle(root, solve_algo=solve_method, solve_config=solve_config, goal_state=None, seed=seed, debug=debug)
    root.mainloop()
