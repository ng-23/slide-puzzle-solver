'''
Testing script
'''

from SlidePuzzle import SlidePuzzle
import tkinter as tk
import argparse
import json
import os
import pandas as pd
import re
from tqdm import tqdm
from dotenv import load_dotenv

def get_args_parser():
    parser = argparse.ArgumentParser(
        prog='Automated Slide Puzzle Solver', 
        description='Solve 3x3 sliding tile puzzle automatically',
        )

    parser.add_argument(
        '--seeds',
        type=str,
        default='1',
        help='Range of random states to control puzzle initialization.',
    )

    parser.add_argument(
        '--solve-algo', 
        type=str, 
        choices=['pc_bfs','pc_dfs','pc_gbfs','pc_astar'], 
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
        '--per-puzzle-results',
        action='store_true',
        help='If specified, save per-puzzle results to individual JSON files',
    )
    
    parser.add_argument(
        '--output-dir', 
        type=str, 
        default='', 
        help='Path to output directory',
        )
    
    return parser

def main(args:argparse.Namespace):
    load_dotenv()

    solve_config = {} if args.solve_config is None else json.load(open(args.solve_config, mode='r'))

    output_dir = args.output_dir
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    root = tk.Tk()

    all_stats = {
        'seed': [],
        'solved': [],
        'solve_time': [],
        'num_moves': [],
    }

    seeds_re = r"^\d+(-\d+)?$" # seeds regex pattern, can either be a single int or a range int-int

    if not re.match(seeds_re, args.seeds):
        raise ValueError(f'Invalid seed string - must be of pattern {seeds_re}')
    
    bounds = args.seeds.split('-')
    lb, ub = int(bounds[0]), None if len(bounds) == 1 else int(bounds[1])+1
    seeds = range(lb, ub if ub is not None else lb+1)

    img_path = os.getenv('PUZZLE_IMG_PATH')
    if img_path is None:
        raise Exception(f'Puzzle image filepath environment variable not found!')

    for seed in tqdm(seeds, desc='Solve Progress'):
        print(f'Puzzle seed: {seed}')
        print(f'Solve algorithm: {args.solve_algo}')
        print(f'Solve config: {solve_config}')

        all_stats['seed'].append(seed)

        puzzle = SlidePuzzle(
            root, 
            img_path,
            solve_algo=args.solve_algo, 
            solve_config=solve_config, 
            seed=seed, 
            debug=args.debug_mode,
            )
        
        res = puzzle.solve_game(simulate=True)
        print(f'Result:\n {res}')
        print('-'*50)

        for metric in res:
            if metric in all_stats:
                all_stats[metric].append(res[metric])

        if args.per_puzzle_results:
            output_path = os.path.join(output_dir, f'puzzle{seed}-{args.solve_algo}.json')
            with open(output_path, mode='w') as f:
                json.dump(res, f, indent=4)

    df = pd.DataFrame.from_dict(all_stats)
    df.to_csv(os.path.join(output_dir, f'{args.solve_algo}-all.csv'), index=False)

if __name__ == '__main__':
    parser = get_args_parser()
    args = parser.parse_args()
    main(args)