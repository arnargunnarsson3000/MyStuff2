from engineer.Algebra.linear import matrix
from sympy import symbols
from sympy.core.symbol import Symbol
from sympy.core.numbers import Float
import sympy
import math
import time
import engineer.GeneralHelp.latex as latex
import engineer.Algebra.linear as linear


#==========================#
#===Elementary Rotations===#
#==========================#
def Rot2d(th=symbols('th')):
    if isinstance(th, Symbol):
        return matrix([[sympy.cos(th), -sympy.sin(th)], [sympy.sin(th), sympy.cos(th)]])
    elif isinstance(th, str):
        return Rot2d(symbols(th))
    else:
        return matrix([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]]).smooth()

def dRot2d(th=symbols('th')):
    if isinstance(th, Symbol):
        return matrix([[-sympy.sin(th), -sympy.cos(th)], [sympy.cos(th), -sympy.sin(th)]])
    elif isinstance(th, str):
        return dRot2d(symbols(th))
    else:
        return matrix([[-math.sin(th), -math.cos(th)], [math.cos(th), -math.sin(th)]]).smooth()

def RotZ(th=symbols('th')):
    if isinstance(th, Symbol):
        return matrix(
            [[sympy.cos(th),-sympy.sin(th), 0],
             [sympy.sin(th), sympy.cos(th), 0],
             [0,0,1]]
        )
    elif isinstance(th, str):
        return RotZ(symbols(th))
    else:
        return matrix(
            [[math.cos(th),-math.sin(th), 0],
             [math.sin(th), math.cos(th), 0],
             [0,0,1]]
        ).smooth()

def RotZ4(th=symbols('th')):
    if isinstance(th, Symbol):
        return matrix(
            [[sympy.cos(th),-sympy.sin(th), 0, 0],
             [sympy.sin(th), sympy.cos(th), 0, 0],
             [0,0,1,0],[0,0,0,1]]
        )
    elif isinstance(th, str):
        return RotZ(symbols(th))
    else:
        return matrix(
            [[math.cos(th),-math.sin(th), 0, 0],
             [math.sin(th), math.cos(th), 0, 0],
             [0,0,1,0],[0,0,0,1]]
        ).smooth()

def RotY(th=symbols('th')):
    if isinstance(th, Symbol):
        return matrix(
            [[sympy.cos(th),0, -sympy.sin(th)],
             [0, 1, 0],
             [sympy.sin(th), 0, sympy.cos(th)]]
        )
    elif isinstance(th, str):
        return RotY(symbols(th))
    else:
        return matrix(
            [[math.cos(th), 0, -math.sin(th)],
             [0, 1, 0],
             [math.sin(th), 0, math.cos(th)]]
        ).smooth()

def RotY4(th=symbols('th')):
    if isinstance(th, Symbol):
        return matrix(
            [[sympy.cos(th),0, -sympy.sin(th), 0],
             [0, 1, 0, 0],
             [sympy.sin(th), 0, sympy.cos(th), 0],[0,0,0,1]]
        )
    elif isinstance(th, str):
        return RotY(symbols(th))
    else:
        return matrix(
            [[math.cos(th), 0, -math.sin(th), 0],
             [0, 1, 0, 0],
             [math.sin(th), 0, math.cos(th), 0],[0,0,0,1]]
        ).smooth()

def RotX(th=symbols('th')):
    if isinstance(th, Symbol):
        return matrix(
            [[1, 0, 0],
             [0, sympy.cos(th), -sympy.sin(th)],
             [0, sympy.sin(th), sympy.cos(th)]]
        )
    elif isinstance(th, str):
        return RotX(symbols(th))
    else:
        return matrix(
            [[1, 0, 0],
             [0, math.cos(th), -math.sin(th)],
             [0, math.sin(th), math.cos(th)]]
        ).smooth()

def RotX4(th=symbols('th')):
    if isinstance(th, Symbol):
        return matrix(
            [[1, 0, 0, 0],
             [0, sympy.cos(th), -sympy.sin(th), 0],
             [0, sympy.sin(th), sympy.cos(th),0], [0,0,0,1] ]
        )
    elif isinstance(th, str):
        return RotX(symbols(th))
    else:
        return matrix(
            [[1, 0, 0, 0],
             [0, math.cos(th), -math.sin(th), 0],
             [0, math.sin(th), math.cos(th), 0], [0,0,0,1]]
        ).smooth()

def RotZd(th):
    return RotZ(math.pi*th/180)

def RotYd(th):
    return RotY(math.pi*th/180)

def RotXd(th):
    return RotX(math.pi*th/180)

def skew(vec):
    if isinstance(vec, matrix):
        return matrix([[0, -vec[2][0], vec[1][0]],
                       [vec[2][0], 0, -vec[0][0]],
                       [-vec[1][0], vec[0][0],0]])
    return matrix([[0, -vec[2], vec[1]],
                   [vec[2], 0, -vec[0]],
                   [-vec[1], vec[0],0]])

def eulerP(e):
    if isinstance(e, list):
        return 2*matrix([[e[0]**2+e[1]**2-0.5, e[1]*e[2]-e[0]*e[3], e[3]*e[1]+e[0]*e[2]],
                        [e[1]*e[2]+e[0]*e[3], e[0]**2+e[2]**2-0.5, e[2]*e[3]-e[0]*e[1]],
                        [e[1]*e[3]-e[0]*e[2], e[2]*e[3]+e[0]*e[1], e[0]**2+e[3]**2-0.5]])
    return 2*matrix([[e[0][0]**2+e[1][0]**2-0.5, e[1][0]*e[2][0]-e[0][0]*e[3][0], e[3][0]*e[1][0]+e[0][0]*e[2][0]],
                     [e[1][0]*e[2][0]+e[0][0]*e[3][0], e[0][0]**2+e[2][0]**2-0.5, e[2][0]*e[3][0]-e[0][0]*e[1][0]],
                     [e[1][0]*e[3][0]-e[0][0]*e[2][0], e[2][0]*e[3][0]+e[0][0]*e[1][0], e[0][0]**2+e[3][0]**2-0.5]])


def A_i(rot, o):
    rot = rot.appendCol(o)
    rot = rot.appendRow([0,0,0,1])
    return rot

def DH(thz, dz, dx, thx):
    tz = matrix(4)
    tz.A[2][3] = dz
    tx = matrix(4)
    tx.A[0][3] = dx
    return RotZ4(thz)*tz*tx*RotX4(thx)

def insert(A, a=None, al=None, d=None, th=None):
    B = A.copy()
    nn = 3
    if a:
        for i in range(A.n):
            for j in range(A.m):
                B[i][j] = preV(B[i][j],a,'a')

    if al:
        for i in range(A.n):
            for j in range(A.m):
                for k in range(len(al)):
                    if al[k]:
                        B[i][j] = preV(B[i][j],al,'al')

    if d:
        for i in range(A.n):
            for j in range(A.m):
                for k in range(len(d)):
                    if d[k]:
                        B[i][j] = preV(B[i][j], d, 'd')

    if th:
        for i in range(A.n):
            for j in range(A.m):
                for k in range(len(th)):
                    if th[k]:
                        B[i][j] = preV(B[i][j], th, 'th')
    
    for i in range(B.n):
        for j in range(B.m):
            B[i][j] = pre(B[i][j])
    # t = time.time()
    #for i in range(B.n):
    #    for j in range(B.m):
    #        B[i][j] = pre(B[i][j])
    # t2 = time.time()
    B = B.simplify()
    # print("simplify time:\t",time.time()-t2)
    #for i in range(B.n):
    #    for j in range(B.m):
    #        B[i][j] = pre(B[i][j])

    # print("time taken:\t", time.time()-t)
    return B

def preV(B, var, l):
    for i in range(len(var)):
        if isinstance(var[i],int) or isinstance(var[i],float):
            try:
                B = B.subs('{}{}'.format(l,i+1), var[i])
            except AttributeError:
                pass
    if not isinstance(B, float) and not isinstance(B, int):
        for arg in B.args:
            arg2 = preV(arg, var, l)
            B = B.subs(arg, arg2)

    return B

def pre(B):
    if isinstance(B, Float):
        if abs(B) - 1 < 0.0001:
            B = int(B)
        else:
            B = round(B,3)
    else:
        try:
            for arg in B.args:
                if isinstance(arg, Float):
                    if abs(arg)-1 < 0.0001:
                        B = B.subs(arg, int(arg))
                    else:
                        B = B.subs(arg, round(arg, 3))
                try:
                    if arg.args:
                        arg2 = pre(arg)
                        B = B.subs(arg, arg2)
                except AttributeError:
                    pass
        except AttributeError:
            pass
    return B


class manipulator:
    """
    A class to design and test robot manipulators
    """
    def __init__(self):
        self.setup = []
        self.nojoints = 0
        self.coord = []
        self.Hmat = matrix(4)

    def addlink(self, type=None):
        i = self.nojoints + 1
        self.nojoints += 1
        d = dict()
        if type:
            d['type'] = type

        d['a'] = symbols('a{}'.format(i))
        d['al'] = symbols('al{}'.format(i))
        d['d'] = symbols('d{}'.format(i))
        d['th'] = symbols('th{}'.format(i))
        d['mat'] = DH(d['th'], d['d'], d['a'], d['al'])
        self.Hmat *= d['mat']
        d['Hmat'] = self.Hmat
        self.setup.append(d)

    def H2(self):
        return self.Hmat

    def H(self):
        A = matrix(4)
        dic = self.setup
        for joint in dic:
            A = A*DH(joint['th'], joint['d'],joint['a'],joint['al'])
        return A

    def Jacobian(self):
        o = []
        z = []
        on = [self.Hmat[i][-1] for i in range(self.Hmat.n-1)]
        for i in range(self.nojoints+1):
            if i == 0:
                z.append([0,0,1])
                o.append([0,0,0])
            else:
                z.append([self.setup[i-1]['Hmat'][j][2] for j in range(self.Hmat.n-1)])
                o.append([self.setup[i-1]['Hmat'][j][3] for j in range(self.Hmat.n-1)])
        Jv = []
        Jw = []
        for i in range(1,self.nojoints+1):
            if self.setup[i-1]['type'] == 'p':
                Jv.append(z[i-1])
                Jw.append([0,0,0])
            else:
                Jv.append(linear.cross(z[i-1], [on[j]-o[i-1][j] for j in range(len(on))]))
                Jw.append(z[i-1])
        Jv = matrix(Jv).t()
        Jw = matrix(Jw).t()
        for each in Jw.A:
            Jv = Jv.appendRow(each)
        return Jv


if __name__ == "__main__":
    man = manipulator()
    man.addlink()
    man.addlink()
    man.addlink()
    man.addlink()
    J4 = man.H()
    J42 = man.H2()
    B = insert(J4, a=[0,0,0,1.15], th=[None,None,math.pi,None], al=[-math.pi/2,math.pi/2,math.pi/2,math.pi/2], d=[1.7,0,None,0])
    B[0][0] = symbols('x1')
    B[1][0] = symbols('x2')
    B[2][0] = symbols('x3')

    B[0][3] = symbols('p1')
    B[1][3] = symbols('p2')
    B[2][3] = symbols('p3')
    print(B)





