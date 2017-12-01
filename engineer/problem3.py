import robotics
from linear import matrix
import math
import latex
from sympy import symbols
import sympy

Ttask0 = matrix([[1,0,0,1.5],[0,1,0,0],[0,0,1,0.2],[0,0,0,1]])  # T_task^0
T0task = Ttask0**-1     # T_0^task
man = robotics.manipulator()
man.addlink()
man.addlink()
man.addlink()
man.addlink()

x1, x2, x3, y1, y2, y3 = symbols('x1 x2 x3 y1 y2 y3')
Tp1 = matrix([[0, x1, y1, 0],[0, x2, y2, -0.5],[-1, x3, y3, 0],[0,0,0,1]])
Tp2 = matrix([[0, x1, y1, 0.35],[0, x2, y2, 0.5],[-1, x3, y3, 0],[0,0,0,1]])
Tp3 = matrix([[0, x1, y1, 0.7],[0, x2, y2, -0.5],[-1, x3, y3, 0],[0,0,0,1]])
Tp4 = matrix([[0, x1, y1, 1.05],[0, x2, y2, 0.5],[-1, x3, y3, 0],[0,0,0,1]])
Tp5 = matrix([[0, x1, y1, 1.4],[0, x2, y2, -0.5],[-1, x3, y3, 0],[0,0,0,1]])

B = robotics.insert(man.H2(), a=[0,0,0,1.15], th=[None,None,math.pi,None], al=[-math.pi/2,math.pi/2,math.pi/2,math.pi/2], d=[1.7,0,None,0])

T0p1 = Ttask0*Tp1
T0p2 = Ttask0*Tp2
T0p3 = Ttask0*Tp3
T0p4 = Ttask0*Tp4
T0p5 = Ttask0*Tp5
f = open('Sols.txt', '+w')
print("__________________________")
EQ = [T0p1[0][0] - B[0][0],
      T0p1[1][0] - B[1][0],
      T0p1[2][0] - B[2][0],
      T0p1[0][3] - B[0][3],
      T0p1[1][3] - B[1][3],
      T0p1[2][3] - B[2][3]]
E1 = sympy.solve(EQ)
print('First')
for each in E1:
    str = ""
    for a in each:
        str += "\t{}:{}".format(a,each[a])
    print(str)
    f.write(str)

print("__________________________")
EQ = [T0p2[0][0] - B[0][0],
      T0p2[1][0] - B[1][0],
      T0p2[2][0] - B[2][0],
      T0p2[0][3] - B[0][3],
      T0p2[1][3] - B[1][3],
      T0p2[2][3] - B[2][3]]
E2 = sympy.solve(EQ)
print('Second')
for each in E2:
    str = ""
    for a in each:
        str += "\t{}:{}".format(a, each[a])
    print(str)
    f.write(str)

print("__________________________")
EQ = [T0p3[0][0] - B[0][0],
      T0p3[1][0] - B[1][0],
      T0p3[2][0] - B[2][0],
      T0p3[0][3] - B[0][3],
      T0p3[1][3] - B[1][3],
      T0p3[2][3] - B[2][3]]
E3 = sympy.solve(EQ)
print('Third')
for each in E3:
    str = ""
    for a in each:
        str += "\t{}:{}".format(a, each[a])
    print(str)
    f.write(str)

print("__________________________")
EQ = [T0p4[0][0] - B[0][0],
      T0p4[1][0] - B[1][0],
      T0p4[2][0] - B[2][0],
      T0p4[0][3] - B[0][3],
      T0p4[1][3] - B[1][3],
      T0p4[2][3] - B[2][3]]
E4 = sympy.solve(EQ)
print('Fourth')
for each in E4:
    str = ""
    for a in each:
        str += "\t{}:{}".format(a,each[a])
    print(str)
    f.write(str)

print("__________________________")
EQ = [T0p5[0][0] - B[0][0],
      T0p5[1][0] - B[1][0],
      T0p5[2][0] - B[2][0],
      T0p5[0][3] - B[0][3],
      T0p5[1][3] - B[1][3],
      T0p5[2][3] - B[2][3]]
E5 = sympy.solve(EQ)
print('Fifth')
for each in E5:
    str = ""
    for a in each:
        str += "\t{}:{}".format(a, each[a])
    print(str)
    f.write(str)
f.close()
print("__________________________")
exit(0)
print(latex.Lmatrix(T0p1, num=['x','y']))
print(latex.Lmatrix(T0p2, num=['x','y']))
print(latex.Lmatrix(T0p3, num=['x','y']))
print(latex.Lmatrix(T0p4, num=['x','y']))
print(latex.Lmatrix(T0p5, num=['x','y']))