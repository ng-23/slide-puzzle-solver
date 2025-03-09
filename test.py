'''
Testing script
'''

from SlidePuzzle import SlidePuzzle
import tkinter as tk
import utils
import argparse
import json

def get_args_parser():
    parser = argparse.ArgumentParser(prog='Puzzle Solver', description='Solve 3x3 tile puzzle')

    parser.add_argument(
        '--seed',
        type=int,
        default=123,
        help='Random state',
    )

    parser.add_argument(
        '--solve-algo', 
        type=str, 
        choices=['pc_bfs'], 
        default='pc_bfs', 
        help='Solve algorithm to use',
        )
    
    parser.add_argument(
        '--solve-config', 
        type=str, 
        default=None, 
        help='Path to JSON config of additional arguments to pass to solve algorithm',
        )
    
    parser.add_argument(
        '--debug-mode', 
        action='store_true', 
        help='If specified, configure puzzle in debug mode',
        )
    
    parser.add_argument(
        '--output-dir', 
        type=str, 
        default='', 
        help='Path to output directory',
        )
    
    return parser

def main(args:argparse.Namespace):
    solve_config = {} if args.solve_config is None else json.load(open(args.sovle_config, mode='r'))

    root = tk.Tk()
    puzzle = SlidePuzzle(
        root, 
        solve_algo=args.solve_algo, 
        solve_config=solve_config, 
        seed=args.seed, 
        debug=args.debug_mode,
        )
    
    root.mainloop()

if __name__ == '__main__':
    parser = get_args_parser()
    args = parser.parse_args()
    main(args)