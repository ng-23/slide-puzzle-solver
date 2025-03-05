import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random
import copy

# for testing, fix the random state
# and put the puzzle in debug/verbose mode
SEED = 123
random.seed(SEED)
DEBUG = True

class SlidePuzzle:
    def __init__(self, root:tk.Tk, debug=False):
        self.root = root
        self.root.title("Image Slide Puzzle")
        self.debug = debug
        
        # Game state
        self.size = 3  # 3x3 grid
        self.buttons = []
        self.current_state = []
        self.empty_pos = None
        self.tile_size = 135  # Size of each tile in pixels
        self.image_tiles = []
        
        # Create UI elements
        # self.load_image()
        self.create_menu()

        self.num_moves = 0
        
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
            i, j = random.choice(possible_moves)
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
        
    def make_move(self, i, j, simulate=False, game_state=None, empty_pos=()) -> None|list[list[int]]:
        # simulate making the move, but don't actually change the board
        if simulate:
            if (i,j) not in self.get_possible_moves(simulate=True, empty_pos=empty_pos):
                return None # invalid move, no valid board
                        
            # move must be valid
            # just swap the empty tile with the tile at the i,j position
            empty_i, empty_j = empty_pos
            empty_tile = game_state[empty_i][empty_j] # actual tile number
            game_state[empty_i][empty_j] = game_state[i][j]
            game_state[i][j] = empty_tile

            return game_state

        # not a simulation - carry out the move and update the board
        # Check if the clicked tile is adjacent to empty space
        if (i, j) in self.get_possible_moves():
            self.num_moves += 1
            self.swap_tiles(i, j)
            self.update_display()
            # Check if puzzle is solved
            if self.check_win():
                messagebox.showinfo("Congratulations!", 
                                  "You solved the puzzle in " +str(self.num_moves) + " moves!")
                
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
        # Check if current state matches solved state
        for i in range(self.size):
            for j in range(self.size):
                expected = i * self.size + j
                if self.current_state[i][j] != expected:
                    return False
        return True
    
    def solve_game(self):
        print("left to students")
        while not self.check_win():
            possible = self.get_possible_moves()
            move = random.choice(possible)
            print(possible)
            print(move)
            self.make_move(move[0],move[1])
            if self.num_moves > 100:
                break

if __name__ == "__main__":
    root = tk.Tk()
    game = SlidePuzzle(root, debug=DEBUG)
    root.mainloop()
