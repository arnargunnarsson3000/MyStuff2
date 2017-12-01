import sys
from PIL import Image
import os
from engineer.Algebra.linear import matrix
import matplotlib.pyplot as plt

class mnum:
    def __init__(self, minx, maxx, miny, maxy, A):
        self.minx = minx
        self.maxx = maxx
        self.maxy = maxy
        self.miny = miny
        self.w = A.m
        self.h = A.n
        self.A = A

def surr0(A):
    temp = matrix(A.n+2, A.m+2)
    for i in range(A.n):
        for j in range(A.m):
            temp[i+1][j+1] = A[i][j]
    return temp

def unsurr(A):
    temp = matrix(A.n-2,A.m-2)
    for i in range(1,A.n-1):
        for j in range(1,A.m-1):
            temp[i-1][j-1] = A[i][j]
    return temp

def through(A, check, x, y, maxx, minx, maxy, miny):
    sum = 4
    if A[y][x] == 2:
        miny = -2
    while sum != 0:
        sum = 0
        if A[y-1][x] != 0 and check[y-1][x] == 0:
            if y-1 < miny:
                miny = y-1
            sum += 1
            check[y - 1][x] = 1
            check, maxx, minx, maxy, miny = through(A, check, x, y - 1, maxx, minx, maxy, miny)
        if A[y+1][x] != 0 and check[y+1][x] == 0:
            if y+1 > maxy:
                maxy = y+1
            sum += 1
            check[y + 1][x] = 1
            check, maxx, minx, maxy, miny = through(A, check, x, y + 1, maxx, minx, maxy, miny)
        if A[y][x-1] != 0 and check[y][x-1] == 0:
            if x-1 < minx:
                minx = x-1
            sum += 1
            check[y][x-1] = 1
            check, maxx, minx, maxy, miny = through(A, check, x-1, y, maxx, minx, maxy, miny)
        if A[y][x+1] != 0 and check[y][x+1] == 0:
            if x+1 > maxx:
                maxx = x+1
            sum += 1
            check[y][x+1] = 1
            check, maxx, minx, maxy, miny = through(A, check, x+1, y, maxx, minx, maxy, miny)
        if A[y + 1][x + 1] != 0 and check[y + 1][x + 1] == 0:
            if x + 1 > maxx:
                maxx = x + 1
            if y + 1 > maxy:
                maxy = y + 1
            sum += 1
            check[y + 1][x + 1] = 1
            check, maxx, minx, maxy, miny = through(A, check, x + 1, y + 1, maxx, minx, maxy, miny)
        if A[y - 1][x - 1] != 0 and check[y - 1][x - 1] == 0:
            if x - 1 < minx:
                minx = x - 1
            if y - 1 < miny:
                miny = y - 1
            sum += 1
            check[y - 1][x - 1] = 1
            check, maxx, minx, maxy, miny = through(A, check, x - 1, y - 1, maxx, minx, maxy, miny)
        if A[y + 1][x - 1] != 0 and check[y + 1][x - 1] == 0:
            if x - 1 < minx:
                minx = x - 1
            if y + 1 > maxy:
                maxy = y + 1
            sum += 1
            check[y + 1][x - 1] = 1
            check, maxx, minx, maxy, miny = through(A, check, x - 1, y + 1, maxx, minx, maxy, miny)
        if A[y - 1][x + 1] != 0 and check[y - 1][x + 1] == 0:
            if x + 1 > maxx:
                maxx = x + 1
            if y - 1 < miny:
                miny = y - 1
            sum += 1
            check[y - 1][x + 1] = 1
            check, maxx, minx, maxy, miny = through(A, check, x + 1, y - 1, maxx, minx, maxy, miny)

    return check, maxx, minx, maxy, miny

def dim(A,x,y, check):
    check, maxx, minx, maxy, miny = through(A, check, x, y,x,x,y,y)
    return minx, maxx, miny, maxy, check

def intersectiony(A):
    ints = []
    for i in range(A.m):
        curr = A[0][i]
        if A.n == 1:
            ints.append(1)
        else:
            count = 0
            if curr == 1: count += 1
            for j in range(A.n):
                temp = A[j][i]
                if temp > curr:
                    count += 1
                curr = A[j][i]

            ints.append(count)
    return ints

def intersectionx(A):
    return intersectiony(A.t())

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

def isZero(A):
    intx = intersectionx(A)
    inty = intersectiony(A)
    # FIRST TEST CHECK NUMBER OF INTERSECTIONS OF HORIZONTAL AND VERTICAL LINES
    intcheckx = []
    intchecky = []
    test = [1,2,1]
    for i in intx:
        if not intcheckx:
            intcheckx.append(i)
        elif i != intcheckx[-1]:
            intcheckx.append(i)
    for i in inty:
        if not intchecky:
            intchecky.append(i)
        elif i != intchecky[-1]:
            intchecky.append(i)
    if intcheckx != test or intchecky != test:
        return False

    # SECOND TEST, SEE WEATHER IT CAN COMPLETE A ROTATION
    curr = A[0][0]
    x = 0
    y = 0
    while x < A.m:
        y = 0
        while y < A.n:
            if curr == 1:
                break
            y = y + 1
            curr = A[y][x]
        if curr == 1:
            break
        x = x + 1
    run = True
    check = matrix(A.n, A.m)
    xc = x
    temp = A.copy()
    try:
        while A[y][xc] != 0:
            temp[y][xc] = 2
            xc += 1
    except IndexError:
        return False

    # break the next layer and iterate through, if anything touches the 2's we have a circle
    # 6, 8, 9 would supposedly pass as well but they don't pass the first test
    xs = 0
    ys = 0
    for i in range(x, xc):
        if A[y-1][i] == 1:
            xc2 = i
            while A[y-1][xc2] != 0:
                temp[y-1][xc2] = 0
                if temp[y-2][xc2] != 0:
                    xs = xc2
                    ys = y-2
                xc2 += 1
            break

    temp = surr0(temp)
    check = surr0(check)
    check,_,_,_,two = through(temp, check, xs, ys, 0, 0, 0, 0)
    if two == -2:
        return True
    return False

def isOne(A):
    t = A.copy()
    h = t.n
    no = int(0.2*h)
    t = matrix(t.A[no:])
    t = matrix(t.A[:t.n-no])
    ll, _ = leftLaser(t)
    if ll[0] == 0:
        return False
    for i in ll:
        if i != ll[0]:
            return False
    ll, _ = rightLaser(t)
    for i in ll:
        if i != ll[0]:
            return False
    return True

def isEight(A):
    intx = intersectionx(A)
    count = 0
    for i in range(len(intx)-1):
        if intx[i+1] == 2:
            intx[i] = 0
        elif intx[i] == 1:
            intx[i] = 0
    intx[-1] = 0
    if sum(intx,0) != 4:
        return False
    xy = []
    for i in range(len(intx)):
        if intx[i] == 2:
            start = False
            for j in range(len(A[i])):
                if A[i][j] == 1:
                    start = True
                if start and A[i][j] == 0:
                    xy.append([j,i])
                    break

    check = matrix(A.n, A.m)
    temp =  matrix(A.n, A.m)
    for i in range(A.n):
        for j in range(A.m):
            if A[i][j] == 1: temp[i][j] = 0
            else: temp[i][j] = 1
    check, _, _, _, _ = through(surr0(temp), surr0(check), 1, 1, 0, 0, 0, 0)
    check, _, _, _, _ = through(surr0(temp), check, 1, A.n, 0, 0, 0, 0)
    check, _, _, _, _ = through(surr0(temp), check, A.m, 1, 0, 0, 0, 0)
    check, _, _, _, _ = through(surr0(temp), check, A.m, A.n, 0, 0, 0, 0)

    if check[xy[0][1]+1][xy[0][0]+1] != 0:
        return False
    if check[xy[1][1]+1][xy[1][0]+1] != 0:
        return False

    return True

def fill(A, check, x, y):
    sum = 4
    while sum != 0:
        sum = 0
        if A[y - 1][x] != 0 and check[y - 1][x] == 0:
            sum += 1
            check[y - 1][x] = 1
            check = fill(A, check, x, y - 1)
        if A[y + 1][x] != 0 and check[y + 1][x] == 0:
            sum += 1
            check[y + 1][x] = 1
            check = fill(A, check, x, y + 1)
        if A[y][x - 1] != 0 and check[y][x - 1] == 0:
            sum += 1
            check[y][x - 1] = 1
            check = fill(A, check, x - 1, y)
        if A[y][x + 1] != 0 and check[y][x + 1] == 0:
            sum += 1
            check[y][x + 1] = 1
            check = fill(A, check, x + 1, y)

        if A[y + 1][x + 1] != 0 and check[y + 1][x + 1] == 0:
            sum += 1
            check[y + 1][x + 1] = 1
            check = fill(A, check, x + 1, y + 1)
        if A[y - 1][x - 1] != 0 and check[y - 1][x - 1] == 0:
            sum += 1
            check[y - 1][x - 1] = 1
            check = fill(A, check, x - 1, y - 1)
        if A[y + 1][x - 1] != 0 and check[y + 1][x - 1] == 0:
            sum += 1
            check[y + 1][x - 1] = 1
            check = fill(A, check, x - 1, y + 1)
        if A[y - 1][x + 1] != 0 and check[y - 1][x + 1] == 0:
            sum += 1
            check[y - 1][x + 1] = 1
            check = fill(A, check, x + 1, y - 1)

    return check

def fillout(A, x=1, y=1):
    temp = surr0(A)
    for i in range(temp.n):
        for j in range(temp.m):
            if temp[i][j] == 1:
                temp[i][j] = 0
            else:
                temp[i][j] = 1
    temp = surr0(temp)

    check = matrix(temp.n,temp.m)

    check = fill(temp, check, x, y)
    return unsurr(unsurr(check))

def isolate(mat):
    check = matrix(mat.n, mat.m)
    k = 0
    for i in range(mat.n):
        for j in range(mat.m):
            if mat[i][j] != 0 and check[i][j] == 0:
                minx, maxx, miny, maxy, check = dim(mat,j,i, check)
                if minx-maxx != 0 :
                    k += 1
                    temp = matrix(mat[miny:maxy+1]).t()
                    temp = matrix(temp[minx:maxx+1]).t()
                    yield minx, maxx, miny, maxy, temp

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

def scalex(A, n):
    S = []
    for i in A.A:
        if 0 not in i or 1 not in i:
            S.append(i*n)
        else:
            s = []
            for j in i:
                s += [j]*n
            S.append(s)
    return matrix(S)

def scaley(A,n):
    return scalex(A.t(), n).t()

def leftLaser(A):
    x = [-1 for i in range(A.n)]
    for i in range(A.n):
        for j in range(A.m):
            if A[i][j] == 1:
                x[i] = j
                break
    u = [-7]
    y = [i for i in reversed(range(len(x)))]
    aveth = 0
    for i in A.A:
        aveth += sum(i,0)/A.n/3


    xx = []
    for i in x:
        if i <= aveth:
            xx.append(0)
            if u[-1] != 'L':
                u.append('L')
        elif i >= 2*aveth:
            xx.append(2)
            if u[-1] != 'H':
                u.append('H')
        else:
            xx.append(1)
            if u[-1] != 'M':
                u.append('M')
    u= u[1:]
    return x, u

def rightLaser(A):
    temp = A.copy()
    for i in range(A.n):
        temp.A[i] = [j for j in reversed(temp.A[i])]
    return leftLaser(temp)

def number(A, heh):
    rl, ru = rightLaser(A)
    ll, lu = rightLaser(A)
    if isMinus(A):
        print('-')
    if isOne(A):
        print(1)
    if isZero(A):
        print(0)
    if lu == ['H','M','L','M','H'] and not isZero(A):
        print(6)
    if ru == ['H','L','M','H'] or ru == ['L','M','H']:
        print(7)

    if ru == ['H','M','L','M','H'] and not isZero(A):
        print(9)
    if isEight(A):
        print(8)

def matsum(A):
    temp = 0
    for i in range(A.n):
        for j in range(A.m):
            temp += A[i][j]
    return temp

def lineV(A):
    """
    boolean function
    :param A: A matrix of a number
    :return: returns True if there is a line that goes from highest to lowest point
    """
    for i in range(A.m):
        if A[-1][i] == 1:
            j = A.n-1
            while j > 0:
                if A[j][i] == 0:
                    break
                else:
                    j -= 1
            if j == 0:
                return True
    return False




if __name__ =="__main__":
    currdir = os.path.realpath(__file__)

    img2 = Image.open('matrixEx.PNG')
    mat2 = matrify(img2)
    nums2 = []
    for minx, maxx, miny, maxy, A in isolate(mat2):
        nums2.append(mnum(minx, maxx, miny, maxy, A))

    img = Image.open('matrixEx2.PNG')
    mat = matrify(img)
    nums = []
    for minx, maxx, miny, maxy, A in isolate(mat):
        nums.append(mnum(minx, maxx, miny, maxy, A))
    sys.setrecursionlimit(2000)
    for i in range(len(nums)):
        temp = fillout(nums[i].A) + nums[i].A
        if matsum(temp) == nums[i].A.n*nums[i].A.m:
            nums[i].pos = [1,2,3,5,7,'-']
            if lineV(nums[i].A):
                nums[i].pos = [1]
            else:
                nums[i].pos = [2,3,5,7,'-']
                if isMinus(nums[i].A):
                    nums[i].pos = ['-']
                else:
                    nums[i].pos = [2,3,5,7]
        else:
            nums[i].pos = [0,4,6,8,9]
            if lineV(nums[i].A):
                nums[i].pos = [4]
            else:
                nums[i].pos = [0,6,8,9]
                if max(intersectiony(nums[i].A)) == 2:
                    nums[i].pos = [0]
                else:
                    nums[i].pos = [6,8,9]
                    # now check where 0 start from top and bottom if ave in higher half, 9, lower half, 6
                    xy = temp.index(0)
                    tempp = fill(temp, temp, xy[0], xy[1])
                    print(tempp)





