import os
import sys
from engineer.Algebra.linear import matrix
from engineer.GeneralHelp import latex
from engineer.GeneralHelp.General import linspace
from engineer.robotics import robotics
from sympy import symbols
import sympy
import math
from math import sin, cos, sqrt, pi
from sympy import sin, cos

import time
import matplotlib.pyplot as plt

def insert(A,t):
    temp = A.copy()
    for i in range(A.n):
        for j in range(A.m):
            temp[i][j] = A[i][j].subs('t', t)
    return temp

def solveABC(A, b):
    q = []
    for i in range(len(b)):
        temp = [b[i], 0, 0]
        abc = A**-1 * matrix([[i] for i in temp])
        abc = [abc[0][0], abc[1][0], abc[2][0]]
        q.append(abc)

    return q

def p4():
    t = symbols('t')
    qi = [t**5, t**4, t**3, t**2, t, t**0]
    dqi = [sympy.diff(i, t) for i in qi]
    ddqi = [sympy.diff(i, t) for i in dqi]
    qi0 = [i.subs(t, 0) for i in qi]
    qi2 = [i.subs(t, 2) for i in qi]

    dqi0 = [i.subs(t, 0) for i in dqi]
    dqi2 = [i.subs(t, 2) for i in dqi]

    ddqi0 = [i.subs(t, 0) for i in ddqi]
    ddqi2 = [i.subs(t, 2) for i in ddqi]
    A = matrix([qi0, qi2, dqi0, dqi2, ddqi0, ddqi2])
    GM_mat = []
    knot = matrix([
        [-0.321750554396642, -4.49454236888801 + 2 * math.pi, 1.61941347407016, 2.92374604209311],
        [0.26396372362570, -4.53174363933971 + 2 * math.pi, 1.94807597387782, 2.96094731254482],
        [-0.223476601140633, -4.55848107238232 + 2 * math.pi, 2.28309001136617, 2.98768474558743],
        [0.193621992855945, -4.57850459598843 + 2 * math.pi, 2.62202212042538, 3.00770826919353],
        [-0.170735211475283, -4.59401022420542 + 2 * math.pi, 2.96352830254749, 3.02321389741052]
    ])
    q = matrix(knot.n-1, knot.m)
    f = open('p4.txt','w+')
    for i in range(1, knot.n):
        lat = []
        for j in range(knot.m):
            sol = A**-1*matrix([knot[i-1][j], knot[i][j], 0, 0, 0, 0]).t()
            str1 = "{}*t**5 + {}*t**4 + {}*t**3 + {}*t**2 + {}*t + {}".format(sol[0][0], sol[1][0], sol[2][0], sol[3][0], sol[4][0], sol[5][0])
            str2 = "{}*t**5 + {}*t**4 + {}*t**3 + {}*t**2 + {}*t + {}".format(round(sol[0][0],3),
                                                                              round(sol[1][0],3),
                                                                              round(sol[2][0],3),
                                                                              round(sol[3][0],3),
                                                                              round(sol[4][0],3),
                                                                              round(sol[5][0],3))
            GM_mat.append(sol.t().A[0])
            q[i-1][j] = str1
            lat.append('q{}{} = '.format(i,j+1) + str2.replace('**','^').replace('*',''))
        f.write(latex.Lcases(lat))
    print("[")
    for each in GM_mat:
        print(str(each)[1:-1]+';')
    print("]")
    f.close()
    return q

def p5():
    t = symbols('t')
    qi = [t ** 5, t ** 4, t ** 3, t ** 2, t, t ** 0]
    dqi = [sympy.diff(i, t) for i in qi]
    ddqi = [sympy.diff(i, t) for i in dqi]
    qi0 = [i.subs(t, 0) for i in qi]
    qi2 = [i.subs(t, 2) for i in qi]

    dqi0 = [i.subs(t, 0) for i in dqi]
    dqi2 = [i.subs(t, 2) for i in dqi]

    ddqi0 = [i.subs(t, 0) for i in ddqi]
    ddqi2 = [i.subs(t, 2) for i in ddqi]
    A = matrix([qi0, qi2, dqi0, dqi2, ddqi0, ddqi2])

    points = [[-0.321750554396642, -4.49454236888801 + 2 * math.pi, 1.61941347407016, 2.92374604209311],
              [0.26396372362570, -4.53174363933971 + 2 * math.pi, 1.94807597387782, 2.96094731254482],
              [-0.223476601140633, -4.55848107238232 + 2 * math.pi, 2.28309001136617, 2.98768474558743],
              [0.193621992855945, -4.57850459598843 + 2 * math.pi, 2.62202212042538, 3.00770826919353],
              [-0.170735211475283, -4.59401022420542 + 2 * math.pi, 2.96352830254749, 3.02321389741052]]
    man = robotics.manipulator()
    man.addlink()
    man.addlink()
    man.addlink()
    man.addlink()
    J4 = man.H2()
    B = robotics.insert(J4, a=[0, 0, 0, 1.15], th=[None, None, math.pi, None],
               al=[-math.pi / 2, math.pi / 2, math.pi / 2, math.pi / 2], d=[1.7, 0, None, 0])

    pxe = str(B[0][-1])        # equation for coordinates of end effector, CONSTANT, in q
    pye = str(B[1][-1])        # equation for coordinates of end effector, CONSTANT, in q
    q = p4()                        # equations for q's, not constant
    # for each segment, evaluate x,y separately.
    # substitute equations from previous problem
    pxy = matrix(4, 2)
    f = open('p5.txt', 'w+')
    GM = []
    for i in range(q.n):
        t = 0
        th1 = eval(q[i][0])
        th2 = eval(q[i][1])
        d3 = eval(q[i][2])
        th4 = eval(q[i][3])
        solx = [eval(pxe)]
        soly = [eval(pye)]
        t = 2
        th1 = eval(q[i][0])
        th2 = eval(q[i][1])
        d3 = eval(q[i][2])
        th4 = eval(q[i][3])
        solx.append(eval(pxe))
        soly.append(eval(pye))
        solx += [0,0,0,0]
        soly += [0,0,0,0]
        ansx = A**-1*matrix(solx).t()
        ansy = A**-1*matrix(soly).t()
        x = "{}*t**5 + {}*t**4 + {}*t**3 + {}*t**2 + {}*t + {}".format(ansx[0][0], ansx[1][0], ansx[2][0], ansx[3][0], ansx[4][0], ansx[5][0])

        y = "{}*t**5 + {}*t**4 + {}*t**3 + {}*t**2 + {}*t + {}".format(ansy[0][0], ansy[1][0], ansy[2][0], ansy[3][0], ansy[4][0], ansy[5][0])

        xr = "{}*t**5 + {}*t**4 + {}*t**3 + {}*t**2 + {}*t + {}".format(round(ansx[0][0], 3),
                                                                        round(ansx[1][0], 3),
                                                                        round(ansx[2][0], 3),
                                                                        round(ansx[3][0], 3),
                                                                        round(ansx[4][0], 3),
                                                                        round(ansx[5][0], 3))

        yr = "{}*t**5 + {}*t**4 + {}*t**3 + {}*t**2 + {}*t + {}".format(round(ansy[0][0],3),
                                                                        round(ansy[1][0],3),
                                                                        round(ansy[2][0],3),
                                                                        round(ansy[3][0],3),
                                                                        round(ansy[4][0],3),
                                                                        round(ansy[5][0],3))
        f.write(latex.Lcases(['px(t) = ' + xr.replace('**', '^').replace('*', ''),
                              'py(t) = ' + yr.replace('**', '^').replace('*', '')]))
        pxy[i][0] = x
        pxy[i][1] = y
        GM.append(ansx.t().A[0])
        GM.append(ansy.t().A[0])
    f.close()
    print("[")
    for each in GM:
        print(str(each)[1:-1] + ';')
    print("]")

    return pxy

def p6():
    man = robotics.manipulator()
    man.addlink('r')
    man.addlink('r')
    man.addlink('p')
    man.addlink('r')
    J = man.Jacobian()
    # print(J)

    B = robotics.insert(J, a=[0, 0, 0, 1.15], th=[None, None, math.pi, None],
                        al=[-math.pi / 2, math.pi / 2, math.pi / 2, math.pi / 2], d=[1.7, 0, None, 0])
    for i in range(B.n):
        for j in range(B.m):
            B[i][j] = str(B[i][j])


    print(latex.Lmatrix(B.simplify(), num=['al','a','th','d']))
    eqa = p4()
    tt = linspace(0, 2, 100)
    eva = []
    pxy = p5()

    for i in range(pxy.n):
        px = []
        py = []
        for j in range(len(tt)):
            t = tt[j]
            px.append(eval(pxy[i][0]))
            py.append(eval(pxy[i][1]))
        plt.plot(px,py, label='segment {}'.format(i+1))
    plt.xlabel('x coordinate')
    plt.ylabel('y coordinate')
    plt.legend()
    plt.show()
    for k in range(eqa.n):
        temp = [[] for i in eqa[k]]
        for i in range(len(eqa[k])):
            for j in range(len(tt)):
                t = tt[j]
                qi = eval(eqa[k][i])
                temp[i].append(qi)
        eva.append(matrix(temp))
    th1v = []
    th2v = []
    d3v = []
    th4v = []
    sing = []
    for mat in eva:
        temp = matrix(B.n, B.m)
        for k in range(len(tt)):     # so here we are splitting the time
            th1 = mat[0][k]
            th2 = mat[1][k]
            d3 = mat[2][k]
            th4 = mat[3][k]
            if th1 < -math.pi or th1 > math.pi:
                print('singularity')
            if th2 < math.pi/6 or th2 > 3*math.pi/4:
                print('singularity')
            if d3 < 1.35 or d3 > 3:
                print('singularity')
            if th4 < -math.pi/2 or th4 > 5*math.pi/4:
                print('singularity')
            th1v.append(th1)
            th2v.append(th2)
            d3v.append(d3)
            th4v.append(th4)

            for i in range(temp.n):
                for j in range(temp.m):
                    temp[i][j] = eval(B[i][j])
            sing.append((temp*temp.t()).det())
            if sing[-1] <= 0 or sing[-1]-int(sing[-1]) < 10**-5:
                print("singularity")

    tv = linspace(0,2, 100) + linspace(2,4, 100) + linspace(4,6, 100) + linspace(6, 8, 100)
    plt.plot(tv, th1v, label='q1')
    plt.plot(tv, th2v, label='q2')
    plt.plot(tv, d3v, label='q3')
    plt.plot(tv, th4v, label='q4')
    plt.xlabel('time    [s]')
    plt.ylabel('q')
    plt.legend()
    plt.show()
    plt.plot(tv, sing)
    plt.xlabel('time    [s]')
    plt.ylabel('Determinant of Jacobian')
    plt.show()

def p7():
    I1 = '0.25*m1*r1**2 + (1/12)*m1*L1**2'
    I1yy = 'm1*r1**2/2'
    I2 = '(m2/12)*(b2**2 + L2**2)'
    I2zz = 'm2*b2**2/6'
    I3 = '(m3/12)*(b3**2 + L3**2)'
    I3yy = 'm3*b3**2/6'
    I4 = 'm4*a4**2/12'
    print(latex.Leq(I1, varname='I1'))
    print(latex.Leq(I1yy, varname='I1yy'))
    print(latex.Leq(I2, varname='I2'))
    print(latex.Leq(I2zz, varname='I2zz'))
    print(latex.Leq(I3, varname='I3'))
    print(latex.Leq(I3yy, varname='I3yy'))
    print(latex.Leq(I4, varname='I4'))
    L1 = 0.7
    r1 = 0.04
    L2 = 1.68
    b2 = 0.2
    L3 = 1.7
    b3 = 0.15
    a4 = 1.02
    m1 = 3
    m2 = 5
    m3 = 3
    m4 = 1
    return eval(I1), eval(I1yy), eval(I2), eval(I2zz), eval(I3), eval(I3yy), eval(I4)

def p9():
    L1 = 0.7
    r1 = 0.04
    L2 = 1.68
    b2 = 0.2
    L3 = 1.7
    b3 = 0.15
    a4 = 1.02
    m1 = 3
    m2 = 5
    m3 = 3
    m4 = 1
    I1, I1yy, I2, I2zz, I3, I3yy, I4 = p7()
    DELTA2 = 0.36
    D = matrix([['D11', 0, 0, 0],
                [0, 'K3 + 2*f1 + f2*sin(q4)', 'f(q4)','2*K1+0.5*f2*sin(q4)'],
                [0, 'f(q4)', 'K4', 'f(q4)'],
                [0, '2*K1+0.5*f2(q3)*sin(q4)','f(q4)','2*K1']])
    D11 = 'K5 + f1-(K2+f1)*cos(2*q2)+K1*cos(2*(q2+q4))-f2*cos(q2+q4)*sin(q2)'
    K0 = 'm2*(0.5*L2-DELTA2)**2 + m3*(0.5*L3)**2'
    K1 = '0.5*(I4 + 0.25*m4*a4**2)'
    K2 = '0.5*(I2-I2zz+I3-I3yy + K0)'
    K3 = 'I2 + I3 + K0 + 2*K1'
    K4 = 'm3+m4'
    K5 = '0.5*(2*I1yy + I2zz + I3yy + K3)'
    f1 = '0.5*K4*q3**2 - 0.5*m3*L3*q3'
    f2 = 'm3*a4*q3'
    f3 = '0.5*a4*m4*cos(q4)'
    q1, q2, q3, q4 = symbols('q1 q2 q3 q4')

    K0 = round(eval(K0), 3)
    K1 = round(eval(K1), 3)
    K2 = round(eval(K2), 3)
    K3 = round(eval(K3), 3)
    K4 = round(eval(K4), 3)
    K5 = round(eval(K5), 3)
    f1 = eval(f1)
    f2 = eval(f2)
    f3 = eval(f3)
    D11 = eval(D11)
    print(latex.Leq(eval(D[0][0]), varname='D_{11}'))
    print(latex.Leq(eval(D[1][1]), varname='D_{22}'))
    print(latex.Leq(eval(D[2][2]), varname='D_{33}'))
    print(latex.Leq(eval(D[3][3]), varname='D_{44}'))
    print(eval(D[3][3]))
    print(latex.Lmatrix(D))
    print(latex.Leq(K0, varname='K0'))
    print(latex.Leq(K1, varname='K1'))
    print(latex.Leq(K2, varname='K2'))
    print(latex.Leq(K3, varname='K3'))
    print(latex.Leq(K4, varname='K4'))
    print(latex.Leq(K5, varname='K5'))
    print(latex.Leq(f1, varname='f1'))
    print(latex.Leq(f2, varname='f2'))
    print(latex.Leq(f3, varname='f3'))
    print(latex.Leq(D11, varname='D_{11}'))

if __name__ == "__main__":
    #print(p4())
    p5()
    #p6()
    #a = p7()
    #for each in a:
    #    print(latex.Leq(each, varname='I_{}'))
    #p9()
