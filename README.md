# Slide Puzzle Solver Assignment

## Overview
In this assignment, you will implement a search algorithm to solve an image-based slide puzzle. The starter code provides a functional slide puzzle game with a GUI, but the solving mechanism currently uses a random search strategy which is inefficient and often fails to find a solution.

Your task is to replace the random search in the `solve_game()` method with an intelligent search algorithm that we've discussed in class (e.g., BFS, DFS, A*, etc.).

## Assignment Goals
- Apply search algorithms to solve a practical problem
- Understand state space representation in puzzles
- Implement heuristic functions for informed search
- Analyze and compare algorithm performance

## Setup
1. Clone the repository
2. Change into the repo's directory, then run `pip install -r requirements.txt` to install the necessary dependencies in `requirements.txt`
3. Create an environment variable file called `.env` - this will store general configuration variables used by some of the scripts
4. In the environment variable file, define a variable called `PUZZLE_IMG_PATH` and set it equal to the absolute path of the puzzle image, like so: `PUZZLE_IMG_FILEPATH = /home/me/img.jpg`
5. Run the `test.py` script from the commandline
   - Specify `-h` to see the optional arguments available (seeds, solve algorithms, output directory, etc.)
   
   Example usage: `python test.py --seeds 1-10 --solve-algo pc_bfs --output-dir ~/results`
