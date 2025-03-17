'''
Miscellaneous utilities
'''

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

def get_vals_map(matrix, size):
    '''
    Construct a dictionary mapping a value in `matrix` to a tuple of its (row,column) position

    Assumes each value in `matrix` is unique - raises an execption otherwise
    '''
    
    vals_map = {}

    for r in range(size):
        for c in range(size):
            val = matrix[r][c]
            if val in vals_map:
                raise ValueError(f'Unique value constraint failed - value {val} is already at position {vals_map[val]} in matrix')
            vals_map[val] = (r,c)
    return vals_map

def calc_2dmanhattan_dist(a:tuple[int,int], b:tuple[int,int]):
    '''
    Calculate the 2D Manhattan Distance between 2 points

    Formula: D = |x1-x2| + |y1-y2|
    '''

    return abs(a[0]-b[0]) + abs(a[1]-b[1])
