from math import pi
from sympy import symbols
import sympy
from sympy.core.symbol import Symbol
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.numbers import NaN
from engineer.Algebra.linear import matrix
import engineer.robotics.robotics as robotics

def Newton_Raphson(eq, var, guess=0, iterations=5):
    if not isinstance(var, Symbol):
        var = symbols(var)
    if isinstance(eq, str):
        eq = parse_expr(eq)

    deq = sympy.diff(eq, var)
    NR = (-eq/deq).simplify()
    for i in range(iterations):
        dx = float(NR.subs(var, guess))
        if isinstance(dx, NaN):
            raise SystemError("Pick a better initial guess, NaN found")
        guess += dx
    return guess

def Newton_Raphson2(eq, var, guess, cvar, cval, iterations=5):
    # Jacobian
    J = matrix(len(eq), len(var))
    for i in range(J.n):
        for j in range(J.m):
            J[i][j] = sympy.diff(eq[i], var[j])
    n = var.index(cvar)
    J = J.delCol(n)
    d = {}
    c = 0
    for i in range(len(var)):
        print(var[i])
        if var[i] == cvar:
            d[var[i]] = cval
        else:
            d[var[i]] = guess[c]
            c += 1

    for ii in range(iterations):
        phi = [i for i in eq]
        for j in range(len(phi)):
            for i in range(len(var)):
                phi[j] = phi[j].subs(var[i], d[var[i]])
        phi = [-float(i) for i in phi]
        nJ = J.copy()
        for key, item in d.items():
            for i in range(J.n):
                for j in range(J.m):
                    nJ[i][j] = nJ[i][j].subs(key, item)
        for i in range(nJ.n):
            for j in range(nJ.m):
                nJ[i][j] = float(nJ[i][j])
        dq = nJ**-1*matrix([[i] for i in phi])

        c = 0
        for key, item in d.items():
            if key != cvar:
                d[key] = item + dq[c][0]
                c += 1
    return d

def Newton_RaphsonA(J, phi, var, guess, iterations=100):
    if isinstance(guess, list):
        guess = matrix(guess).t()
    for ii in range(iterations):
        nphi = [i for i in phi]
        for i in range(len(phi)):
            for j in range(len(var)):
                nphi[i] = nphi[i].subs(var[j], guess[j][0])
        nphi = [-i for i in nphi]
        nJ = J.copy()
        for k in range(len(var)):
            for i in range(nJ.n):
                for j in range(nJ.m):
                    nJ[i][j] = nJ[i][j].subs(var[k], guess[k][0])
        for i in range(nJ.n):
            for j in range(nJ.m):
                nJ[i][j] = float(nJ[i][j])
        dq = nJ**-1*matrix(nphi).t()
        guess = dq + guess
        if dq.tsum() < 10**-5:
            break
    return guess


if __name__ == "__main__":
    # eq = "x**3 + 2*x - 7"
    # eq = parse_expr(eq)
    # zero = Newton_Raphson(eq, 'x', guess=5, iterations=20)
    # eq = ["10*cos(th1) + 2*cos(th2) - d", "10*sin(th1)+2*sin(th2) - 4"]
    # eq = [parse_expr(i) for i in eq]
    # var = ['th1', 'th2', 'd']
    # guess = Newton_Raphson2(eq, var, [0.1,1], 'th1', pi*30/180, iterations=100)
    x = []
    y = []
    th = []
    rho1 = 0.15
    rho4 = 0.06
    st = matrix([[-0.5,-0.05],
                [0.5, -0.05],
                [0, -0.15],
                [0.44, 0.1512461],
                [-0.05, 0.5],
                [-0.05, 0],
                [0.5, 0],
                [0, -0.06]
                ])
    for i in range(5):
        x.append(symbols('x{}'.format(i+1)))
        y.append(symbols('y{}'.format(i+1)))
        th.append(symbols('th{}'.format(i+1)))
    r = []
    for i in range(5):
        r.append(matrix([x[i],y[i]]).t())
    s = []
    for i in range(st.n):
        s.append(matrix(st[i]).t())
    A3 = robotics.Rot2d(th[2])
    A5 = robotics.Rot2d(th[4])
    phi1 = r[0] - r[2] - A3*s[0]
    phi2 = r[1] - r[2] - A3*s[1]
    phi3 = r[3] - r[2] - A3*s[3]
    phi4 = r[4] + A5*s[6] - r[2] - A3*s[4]
    phi5 = r[0] - matrix([0, rho1]).t() + matrix([th[0]*rho1, 0]).t()
    phi6 = r[1] - matrix([1, rho1]).t() + matrix([th[1]*rho1, 0]).t()
    phi7 = rho1*th[1] + rho4*th[3]
    phi8 = x[0]
    phi9 = (r[2] + A3*s[5] - r[4]).t()*(r[2] + A3*s[5] - r[4]) - 0.5**2
    phi = [phi1[0][0], phi1[1][0],
           phi2[0][0], phi2[1][0],
           phi3[0][0], phi3[1][0],
           phi4[0][0], phi4[1][0],
           phi5[0][0], phi5[1][0],
           phi6[0][0], phi6[1][0],
           phi7,
           phi8,
           phi9]
    # ex lecture 5 start
    t = symbols('t')
    phi[-2] = th[3] - 7 / 100 * t ** 3
    phi[-1] = (r[2] + A3 * s[5] - r[4]).t() * (r[2] + A3 * s[5] - r[4]) - (0.5 + t ** 3 / 4000)
    # ex lecture 5 end
    J = []
    for i in range(len(phi)):
        temp = []
        for j in range(len(x)):
            temp.append(sympy.diff(phi[i], x[j]))
            temp.append(sympy.diff(phi[i], y[j]))
            temp.append(sympy.diff(phi[i], th[j]))
        J.append(temp)
    J = matrix(J)
    guess = [0, 0.11, 0, 0.9, 0.11, 0, 0.45, 0.11, 0, 0.8, 0.2, 0, 0.3, 0.3, 0.3]
    var = []
    for i in range(len(x)):
        var.append(x[i])
        var.append(y[i])
        var.append(th[i])
    # Newton_RaphsonA(J, phi, var, guess)
    print(phi[6])
    print(phi[-1])
    print(phi[-2])






