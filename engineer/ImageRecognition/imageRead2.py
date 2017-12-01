import sys
from PIL import Image
import os
from engineer.Algebra.linear import matrix
import matplotlib.pyplot as plt
from engineer.ImageRecognition.imageRead import isolate, intersectionx, intersectiony

def matrify(img):
    w, h = img.size
    px = img.load()
    mat = matrix(h, w)
    for i in range(h):
        for j in range(w):
            if (255, 255, 255, 255) != px[j, i] \
                    and (242, 242, 242, 255) != px[j, i] \
                    and (238, 238, 238, 255) != px[j, i]:
                mat[i][j] = 1
    return mat

def checkN(A, key, row, col):
    return A[row-1][col] == key

def checkS(A, key, row, col):
    return A[row+1][col] == key

def checkW(A, key, row, col):
    return A[row][col-1] == key

def checkE(A, key, row, col):
    return A[row][col+1] == key

def checkNW(A, key, row, col):
    return A[row-1][col-1] == key

def checkNE(A, key, row, col):
    return A[row-1][col+1] == key

def checkSW(A, key, row, col):
    return A[row+1][col-1] == key

def checkSE(A, key, row, col):
    return A[row+1][col+1] == key

def checkSurr(A, key, row, col):
    """
    Checks to see if the key is in the surrounding
    :param A: matrix
    :param key: number
    :return: True if key is to the left, right, above or below
    """
    if row != 0:
        if checkN(A, key, row, col):
            return True
    if col != 0:
        if checkW(A, key, row, col):
            return True
    if row != A.n-1:
        if checkS(A, key, row, col):
            return True
    if col != A.m-1:
        if checkE(A, key, row, col):
            return True
    return False

def blobify(A):
    temp = matrix(A.n,A.m)
    for i in range(A.n):
        for j in range(A.m):
            if A[i][j] == 1 and checkSurr(A, 0, i, j):
                temp[i][j] = 1
    return temp

def edge(A):
    temp = matrix(A.n, A.m)
    for i in range(A.n):
        for j in range(A.m):
            if A[i][j] == 1:
                tot = 0
                if i != 0:
                    if checkN(A, 0, i, j):
                        tot += 1
                if j != 0:
                    if checkW(A, 0, i, j):
                        tot += 1
                if i != A.n - 1:
                    if checkS(A, 0, i, j):
                        tot += 1
                if j != A.m - 1:
                    if checkE(A, 0, i, j):
                        tot += 1
                if tot >= 2:
                    temp[i][j] = 1
    return temp

def edge8(A):
    temp = matrix(A.n, A.m)
    for i in range(A.n):
        for j in range(A.m):
            if A[i][j] == 1:
                tot = 0
                if i != 0:
                    if checkN(A, 0, i, j):
                        tot += 1
                if j != 0:
                    if checkW(A, 0, i, j):
                        tot += 1
                if i != A.n - 1:
                    if checkS(A, 0, i, j):
                        tot += 1
                if j != A.m - 1:
                    if checkE(A, 0, i, j):
                        tot += 1
                if i != 0 and j != 0:
                    if checkNW(A, 0, i, j):
                        tot += 1
                if i != A.n-1 and j != 0:
                    if checkSW(A, 0, i, j):
                        tot += 1
                if i != A.n-1 and j != A.m-1:
                    if checkSE(A, 0, i, j):
                        tot += 1
                if i != 0 and j != A.m-1:
                    if checkNE(A, 0, i, j):
                        tot += 1
                if tot >= 4:
                    temp[i][j] = 1
    return temp

def isMinus(A):
    intx = intersectionx(A)
    inty = intersectiony(A)
    for i in intx:
        if i > 1:
            return False
    for i in inty:
        if i > 1:
            return False
    return True

def whatNumber(A):
    # first fill test
    pass


if __name__ == "__main__":
    currdir = os.path.realpath(__file__)

    img = Image.open('matrixEx2.PNG')
    mat = matrify(img)

    nums = []
    for _,_,_,_, trix in isolate(mat):
        nums.append(trix)
    for each in nums:
        blob = blobify(each)
        x = []
        y = []
        for i in range(each.n):
            for j in range(each.m):
                if blob[i][j] == 1:
                    x.append(j)
                    y.append(-i)
        plt.plot(x, y, '*')
        edge1 = edge(each)
        x = []
        y = []
        for i in range(each.n):
            for j in range(each.m):
                if edge1[i][j] == 1:
                    x.append(j)
                    y.append(-i)
        plt.plot(x, y, '*')
        edge2 = edge8(each)
        x = []
        y = []
        for i in range(each.n):
            for j in range(each.m):
                if edge2[i][j] == 1:
                    x.append(j)
                    y.append(-i)
        plt.plot(x, y, '*')
        plt.show()