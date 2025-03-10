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
