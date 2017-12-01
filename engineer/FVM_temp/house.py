import sys
import os
import time
from engineer.Algebra.linear import matrix
from engineer.ImageRecognition.imageRead import surr0
import math
import matplotlib.pyplot as plt

class House:
    """
    A class for designing a house
    """

    def __init__(self, x1, x2, h, w, acc=20):
        sys.stdout.write('\r INITIALIZING HOUSE DESIGN...')
        ttt = time.time()

        scale = acc
        self.scale = scale
        self.acc = acc
        self.roof = False
        self.chimney = False
        x3 = x2

        x1 = int(x1*scale)
        x2 = int(x2*scale)
        x3 = int(x3*scale)
        h = int(h*scale)
        w = int(w*scale)
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.w = w
        self.h = h
        self.fh = h
        mesh = matrix(h, w)
        for i in range(mesh.n):
            for j in range(mesh.m):

                if j < x1:     mesh[i][j] = 1   # when within first wall thickness all x,y are 1
                elif j > w-1-x2: mesh[i][j] = 1   # when within the right wall thickness all x,y are 1
                elif i < x3:     mesh[i][j] = 1   # when within the roof all x,y are 1
                else:             mesh[i][j] = -1  # inside of wall gets -1 value to help with knowing where inside is, maybe not needed

        self.mesh = mesh
        self.atmat = 1
        self.floor = [mesh]
        sys.stdout.write('\r INITIALIZING HOUSE DESIGN... DONE! {}\n'.format(time.time()-ttt))

    def rmesh(self):
        mesh = self.mesh.copy()
        mesh = surr0(mesh)
        mesh = surr0(mesh)
        mesh = surr0(mesh)
        mesh = surr0(mesh)
        mesh = mesh.delRow(mesh.n - 1)
        mesh = mesh.delRow(mesh.n - 1)
        mesh = mesh.delRow(mesh.n - 1)
        mesh = mesh.delRow(mesh.n - 1)
        mesh = mesh.appendRow(-2)
        mesh = mesh.appendRow(-2)
        mesh = mesh.appendRow(-2)
        mesh = mesh.appendRow(-2)
        return mesh

    def plot_house(self, mesh=None):
        sys.stdout.write('\r PLOTTING HOUSE...')
        ttt = time.time()
        if not mesh:
            mesh = self.rmesh()

        xg = []
        yg = []
        xo = []
        yo = []
        xi = []
        yi = []
        for i in range(mesh.n):
            for j in range(mesh.m):

                if mesh[i][j] == -2:
                    xg.append(j)
                    yg.append(mesh.n-i)
                if mesh[i][j] == -1:
                    xi.append(j)
                    yi.append(mesh.n-i)
                if mesh[i][j] == 0:
                    xo.append(j)
                    yo.append(mesh.n - i)
        plt.plot(xo, yo, '*', label='outside')
        plt.plot(xg, yg, '*', label='ground')
        plt.plot(xi, yi, '*', label='inside')

        for k in range(1, mesh.max()+1):
            x = []
            y = []
            for i in range(mesh.n):
                for j in range(mesh.m):
                    if mesh[i][j] == k:
                        x.append(j)
                        y.append(mesh.n - i)
            plt.plot(x, y, '*', label='material {}'.format(k))

        plt.legend()
        plt.show()
        sys.stdout.write('\r PLOTTING HOUSE... DONE! {}\n'.format(time.time() - ttt))

    def add_floor(self, h=None, w=None, start=None, stop=None, material=1):
        sys.stdout.write('\r ADDING FLOOR...')
        ttt = time.time()
        if self.atmat < material:
            self.atmat = material
        if not h:
            h = self.fh
        if not w:
            w = self.w
        else:
            w = int(w*self.scale)
        if not start:
            start = 0
        if not stop:
            stop = w

        if start != 0:
            tmesh = matrix([[0 for j in range(start)] for i in range(h)])
            for i in range(self.x1):
                tmesh.appendCol(material)
        else:
            tmesh = matrix([[material for j in range(self.x1)] for i in range(h)])

        for i in range(w-self.x1-self.x2):
            col = [material for j in range(self.x3)] + [-1 for j in range(self.mesh.n-self.x3)]
            tmesh = tmesh.appendCol(col)
        for i in range(self.x2):
            tmesh = tmesh.appendCol(1)
        for i in range(self.mesh.m-tmesh.m):
            tmesh = tmesh.appendCol(0)
        self.floor.append(tmesh)
        for i in self.mesh.A:
            tmesh = tmesh.appendRow(i)
        self.w = tmesh.m
        self.h = tmesh.n
        self.mesh = tmesh
        sys.stdout.write('\r ADDING FLOOR... DONE! {}\n'.format(time.time() - ttt))

    def add_roof(self, h=None, thickness=None, material=1):
        sys.stdout.write('\r ADDING ROOF...')
        ttt = time.time()
        if not self.roof:
            if material > self.atmat:
                self.atmat = material
            if not h:
                h = self.fh
            if not thickness:
                thickness = self.x3
            temp = matrix(h, math.ceil(self.w/2))
            for i in range(temp.n):
                for j in range(temp.m):
                    if int(-2*h*j/self.w + temp.n) <= i and int(-2*h*j/self.w + temp.n + (h**2+0.25*self.w**2)**0.5*thickness/h*self.w/(2*(h**2 + 0.25*self.w**2)**0.5)) >= i:
                        temp[i][j] = material
                    elif int(-2 * h * j / self.w + temp.n + (h ** 2 + 0.25 * self.w ** 2) ** 0.5 * thickness / h * self.w / (
                    2 * (h ** 2 + 0.25 * self.w ** 2) ** 0.5)) < i:
                        temp[i][j] = -1

            other = temp.copy()
            if self.w % 2 == 1:
                other = other.delCol(-1)
            other = other.flipLR().t()
            for i in range(other.n):
                temp = temp.appendCol(other[i])
            self.floor.append(temp)
            for i in self.mesh.A:
                temp = temp.appendRow(i)
            self.mesh = temp
            self.h = temp.n
            self.w = temp.m
            self.roof = True
        sys.stdout.write('\r ADDING ROOF... DONE!{} \n'.format(time.time() - ttt))

    def add_chimney(self, lor='r', thickness=None, material=1, w=None):
        sys.stdout.write('\r ADDING CHIMNEY...')
        ttt = time.time()
        if not self.chimney:
            if self.atmat < material:
                self.atmat = material
            if lor == 'r':
                lor = [math.ceil(self.w/2), self.w]
            else:
                lor = [0, math.floor(self.w/2)]
            if not w:
                w = int(abs(lor[0]-lor[1])/4)
            if not thickness:
                thickness = math.ceil(w/6)
            start = int(abs(lor[0]+lor[1])/2 - w/2)
            temp = self.floor[-1].copy()
            for j in range(start, start+thickness):
                i = 0
                while temp[i][j] == 0:
                    temp[i][j] = material
                    i += 1
            for j in range(start+thickness, start+w-thickness):
                i = 0
                while temp[i][j] != -1:
                    temp[i][j] = material+1
                    i += 1
            for j in range(start+w-thickness, start+w):
                i = 0
                while temp[i][j] == 0:
                    temp[i][j] = material
                    i += 1
            self.atmat += 1
            self.floor[-1] = temp.copy()
            self.update()
            self.chimney = True
        sys.stdout.write('\r ADDING CHIMNEY... DONE! {}\n'.format(time.time() - ttt))

    def update(self):
        sys.stdout.write('\r UPDATING MESH...')
        ttt = time.time()
        temp = []
        for i in reversed(self.floor):
            for j in i.A:
                temp.append(j)
        self.mesh = matrix(temp).copy()
        sys.stdout.write('\r UPDATING MESH... DONE! {}\n'.format(time.time() - ttt))

    def add_radiator(self):
        """
        Adds radiator to house, electric heater
        :return:
        """
        print(self.mesh.size())
        for i in range(int(self.mesh.n/2+self.mesh.n/6), self.mesh.n):
            for j in range(int(self.mesh.m/2-self.mesh.m/8), int(self.mesh.m/2+self.mesh.m/8)):
                self.mesh[i][j] = -3

    def make_block(self, h, w, acc):
        """
        Makes a block for testing
        :param h:
        :param w:
        :param acc:
        :return:
        """
        mesh = matrix(h*acc, w*acc)
        for i in range(mesh.n):
            for j in range(mesh.m):
                mesh[i][j] = 1
        self.mesh = mesh.copy()

if __name__ == "__main__":
    hous = House(0.5, 0.5, 2, 4, acc=4)
    hous.add_radiator()
    print(hous.rmesh())

