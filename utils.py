'''
Miscellaneous utilities
'''

import copy

def tuplify_2dmatrix(matrix):
    '''
    Convert 2D matrix to tuple of tuples
    '''

    return tuple([tuple(row) for row in matrix])

def listify_2dmatrix(matrix):
    '''
    Convert 2D matrix to list of lists
    '''

    return list([list(row) for row in matrix])

class UniqueGrid():
    '''
    2D grid space with added unique value constraint at every position
    '''

    def __init__(self, size:int=3):
        self.size = size
        self.space = self.gen_space()
        self.index, self.reverse_index = self.build_index()

    def gen_space(self):
        space = []

        for r in range(self.size):
            row = []
            for c in range(self.size):
                row.append(r * self.size + c)
            space.append(row)

        self.space = space

        return space
    
    def build_index(self):
        index = {} # maps a coordinate pair to its value in the grid

        for r in range(self.size):
            for c in range(self.size):
                index[tuple([r,c])] = self.space[r][c]

        reverse_index = {}
        for pos,val in index.items():
            if val not in reverse_index:
                reverse_index[val] = pos
            else:
                raise ValueError(f'Unique value constraint failed - value {val} is already in grid space at position {reverse_index[val]}')

        return index, reverse_index
    
    def insert(self, pos, val):
        if val in self.reverse_index:
            raise ValueError(f'Unique value constraint failed - value {val} is already in grid space at position {self.reverse_index[val]}')
        
        r, c = pos
        prev_val = self.space[r][c]
        self.space[r][c] = val
        self.index[tuple([r,c])] = val

        return prev_val
    
    def swap(self, old_pos, new_pos):
        if old_pos not in self.index:
            raise ValueError(f'Position {old_pos} out of range')
        if new_pos not in self.index:
            raise ValueError(f'Position {new_pos} out of range')

        swap_val = self.index[old_pos]
        with_val = self.index[new_pos]

        self.space[old_pos[0]][old_pos[1]] = with_val
        self.space[new_pos[0]][new_pos[1]] = swap_val

        self.index[old_pos] = with_val
        self.index[new_pos] = swap_val

        self.reverse_index[with_val] = old_pos
        self.reverse_index[swap_val] = new_pos

    def get_val(self, pos):
        return None if pos not in self.index else self.index[pos]
    
    def get_pos(self, val):
        return (-1,-1) if val not in self.reverse_index else self.reverse_index[val]

    def get_space(self, tuplify=False):
        space = copy.deepcopy(self.space)

        return tuplify_2dmatrix(space) if tuplify else space
    
    def set_space(self, space):
        prev_space = copy.deepcopy(self.space)

        self.space = space
        try:
            self.build_index()
        except Exception as e:
            self.space = prev_space
            raise e

        return prev_space

    def __str__(self):
        s = ''

        # see https://stackoverflow.com/a/63496125/ (pretty printing the 2d matrix)
        for r in self.space:
            s = s + f'{' '*3}'.join(map(str, r)) + '\n'

        return s
    
if __name__ == '__main__':
    g = UniqueGrid(size=3)
    print(g)

    pos = (0,0)
    new_val = 5
    try:
        _ = g.insert(pos, new_val)
    except Exception as e:
        print(f'Insertion failed: {e}')

    new_val = 777
    prev_val = g.insert(pos, new_val)
    print(f'Previous value at {pos} was {prev_val}, new value is {new_val}')

    new_space = [
        [0,1,1],
        [2,3,4],
        [5,6,7],
    ]
    try:
        _ = g.set_space(new_space)
    except Exception as e:
        print(f'Set space failed: {e}')

    print(g.get_space(tuplify=True))

    old_pos = (0,0)
    new_pos = (1,1)
    g.swap(old_pos, new_pos)
    print(g)
    
