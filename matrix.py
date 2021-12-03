from itertools import starmap, product
from operator import mul

# faster version using built in python modules for dot product:
#from: https://stackoverflow.com/questions/1828233/optimized-dot-product-in-python
def dotProduct(v1, v2):
    return sum(starmap(mul, zip(v1, v2)))

def matCol(A, colIdx):
    # Gets the colIdx^th column from a matrix
    return [row[colIdx] for row in A]

def matMul(A, B):
    # Verify the matrices have a NIL dimension
    rowsA, rowsB = len(A), len(B)
    if rowsA == 0 or rowsB == 0:
        return None
    
    colsA, colsB = len(A[0]), len(B[0])
    if colsA == 0 or colsB == 0:
        return None
    
    # Verify the multiplication can be done
    if colsA != rowsB:
        return None

    res = [[0]*colsB for _ in range(rowsA)]
    for i, j in list(product(*[range(rowsA), range(colsB)])):
        res[i][j] = dotProduct(A[i], matCol(B, j))
    
    return res


def transpose(A):
    # Transposes a matrix
    if A != []:
        rowsA, colsA = len(A), len(A[0])   
        res = [[0]*rowsA for _ in range(colsA)]
        for i in range(rowsA):
            for j in range(colsA):
                res[j][i] = A[i][j]

        return res

def matDet2D(A):
    # Computes the determinant of a 2x2 matrix
    if len(A) != 2 or len(A[0]) != 2:
        return None

    return (A[0][0] * A[1][1]) - (A[0][1] * A[1][0])


def matInv2D(A):
    # Computes the determinant of a 2x2 matrix
    if len(A) != 2 or len(A[0]) != 2:
        return None

    c = 1 / matDet2D(A)

    return [[c*A[1][1], -c*A[0][1]],
            [-c*A[1][0], c*A[0][0]]]


def printMatrix(A):
    # Prints all the rows in a matrix
    print('Matrix:')
    for row in A:
        print(f'   {row}')