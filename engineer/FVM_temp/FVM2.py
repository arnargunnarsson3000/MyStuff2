import matplotlib.pyplot as plt
from engineer.Algebra.linear import *
import os, sys
import time
import math
import sqlite3
from engineer.FVM_temp.house2 import House

import engineer.SQLbeast.sql_class as sqls

#TODO: below
#       -different kinds of meshes
#           - add chimney or window
#       -include more realistic variables
#           - radiation
#           - convection

No = -1
So = 1
We = -1
Ea = 1

class fvm:
    """
    finite volume method for assignment 5
    In mesh:
        positive integers are wall
        0 is outside
        -1 is inside
        -2 is ground
    """
    db = os.path.join(os.path.dirname(__file__),"TEMP_MESH.db")
    propmesh_init = False

    def __init__(self, mesh=None,
                 T=None, k=None, cp=None, rho=None, const=None, scale=1,
                 project=None, house_class=None):

        self.Trad = 300
        self.cp_rad = 3000
        self.k_rad = 4
        self.rho_rad = 800
        self.T = T
        self.k = k
        self.cp = cp
        self.rho = rho
        self.const = const
        self.project = project
        self.scale = scale
        self.d = 1/scale
        self.mesh = mesh
        self.house_class = house_class
        self.sql = sqls.sql_cmds(db=self.db, project=project)
        self.propmesh()
        self.setup_project_db()
        self.c_vec()


    def setup_project_db(self):
        sql = self.sql
        conn, curs = sql.cc()
        sql.create_table(curs, self.project, 'tables')
        sql.create_table(curs, 'data', ['iteration', 'array'])
        sql.create_table(curs, 'savestate', ['ii', 'iii', 'Tnew', 'Tmesh'])
        sql.create_table(curs, 'cvec', ['c', 'cW', 'cN', 'cE', 'cS'])
        sql.create_table(curs, 'rho', ["vals%d"%i for i in range(len(self.rho))])
        sql.create_table(curs, 'k', ["vals%d"%i for i in range(len(self.rho))])
        sql.create_table(curs, 'cp', ["vals%d"%i for i in range(len(self.rho))])
        sql.create_table(curs, 'T', ["vals%d"%i for i in range(len(self.rho))])
        sql.create_table(curs, 'other', ["vals%d"%i for i in range(len(self.rho))])
        for each in sql.list_tables(curs):
            print(each)
        print(self.db)
        sql.insert_table(curs, 'rho', self.rho)
        sql.insert_table(curs, 'k', self.k)
        sql.insert_table(curs, 'cp', self.cp)
        sql.insert_table(curs, 'T', self.T)

        sql.save_status(curs)
        sql.ccc(conn)


    def propmesh(self):
        sys.stdout.write('\r CREATING PROPERTY MESH.....')
        ttt = time.time()
        mesh = self.mesh.copy()
        Kmesh = self.mesh.copy()
        Cmesh = self.mesh.copy()
        Rmesh = self.mesh.copy()
        Smesh = matrix(Kmesh.n, Kmesh.m)
        Tmesh = self.mesh.copy()
        for i in range(Kmesh.n):
            for j in range(Kmesh.m):
                Smesh[i][j] = ''
                Kmesh[i][j] = self.k[mesh[i][j]]
                Cmesh[i][j] = self.cp[mesh[i][j]]
                Rmesh[i][j] = self.rho[mesh[i][j]]
                Tmesh[i][j] = self.T[mesh[i][j]]

        for i in range(Kmesh.n):
            for j in range(Kmesh.m):
                if self.mesh[i][j] > 0:
                    comp = mesh[i][j]
                    if mesh[i-1][j] != comp: Smesh[i][j] += 'N'
                    if mesh[i+1][j] != comp: Smesh[i][j] += 'S'
                    if mesh[i][j+1] != comp: Smesh[i][j] += 'E'
                    if mesh[i][j-1] != comp: Smesh[i][j] += 'W'

        self.Smesh = Smesh.copy()
        self.Kmesh = Kmesh
        self.Cmesh = Cmesh
        self.Rmesh = Rmesh
        self.Tinit = Tmesh.copy()   # temperature mesh at time = 0 [s]
        self.Tmesh = Tmesh.copy()
        self.Tnew = Tmesh.copy()
        dt_poss = []
        for i in range(len(self.const)):
            if self.const[i] == 0:
                dt_poss.append(i)

        self.dt = min([self.d ** 2 / (4 * self.k[i] / (self.cp[i] * self.rho[i])) for i in dt_poss]) / 1.2
        self.iii = 0
        self.iis = 0
        sys.stdout.write('\r CREATING PROPERTY MESH..... DONE! {}\n'.format(time.time()-ttt))

    def c_vec(self):


        d = self.d
        c = []
        cW = []
        cE = []
        cN = []
        cS = []
        n = self.mesh.n
        m = self.mesh.m
        mesh = self.mesh
        const = self.const
        Rmesh = self.Rmesh
        Cmesh = self.Cmesh
        Kmesh = self.Kmesh
        dt = self.dt
        for i in range(n):
            for j in range(m):
                if self.mesh[i][j] > 0:
                    c.append(Rmesh[i][j] * Cmesh[i][j] * d * d / dt)  # constant left side
                    if mesh[i][j-1] != mesh[i][j]:
                        cW.append(1 / (0.5 / Kmesh[i][j]))
                    else:
                        cW.append(1 / (0.5 / Kmesh[i][j - 1] + 0.5 / Kmesh[i][j]))
                    if mesh[i][j + 1] != mesh[i][j]:
                        cE.append(1 / (0.5 / Kmesh[i][j]))
                    else:
                        cE.append(1 / (0.5 / Kmesh[i][j] + 0.5 / Kmesh[i][j + 1]))
                    if mesh[i-1][j] != mesh[i][j]:
                        cN.append(1 / (0.5 / Kmesh[i][j]))
                    else:
                        cN.append(1 / (0.5 / Kmesh[i - 1][j] + 0.5 / Kmesh[i][j]))
                    if mesh[i + 1][j] != mesh[i][j]:
                        cS.append(1 / (0.5 / Kmesh[i][j]))
                    else:
                        cS.append(1 / (0.5 / Kmesh[i][j] + 0.5 / Kmesh[i + 1][j]))

        self.c = c
        self.cN = cN
        self.cW = cW
        self.cS = cS
        self.cE = cE
        d = self.d
        cWf = []
        cEf = []
        cNf = []
        cSf = []
        Smesh = self.Smesh
        cR = []
        lcR = 0
        self.lenRoofO = self.house_class.roof_len_out
        self.lenRoofI = self.house_class.roof_len_in
        self.dict_OI = {}
        for i in range(n):
            for j in range(m):
                if self.mesh[i][j] > 0:
                    if 'N' in Smesh[i][j]:
                        cNf.append("{d} / (R + 0.5 * {d} / {kij})".format(d=d,
                                                                          kij=Kmesh[i][j],
                                                                          kim1j=Kmesh[i-1][j]))
                    else:
                        cNf.append(d / (0.5 * d / Kmesh[i - 1][j] + 0.5 * d / Kmesh[i][j]))
                    if 'S' in Smesh[i][j] and mesh[i][j] != -2:
                        cSf.append("{d} / (R +0.5 * {d} / {kij})".format(d=d,
                                                                         kij=Kmesh[i][j],
                                                                         kip1j=
                                                                         Kmesh[i + 1][j]))
                    else:
                        cSf.append(d / (0.5 * d / Kmesh[i][j] + 0.5 * d / Kmesh[i + 1][j]))
                    if 'W' in Smesh[i][j]:
                        cWf.append("{d} / (R +0.5 * {d} / {kij})".format(d=d,
                                                                         kij=Kmesh[i][j],
                                                                         kijm1=Kmesh[i][j - 1]))
                    else:
                        cWf.append(d / (0.5 * d / Kmesh[i][j - 1] + 0.5 * d / Kmesh[i][j]))
                    if 'E' in Smesh[i][j]:
                        cEf.append("{d} / (0.5 * {d} / {kij} + R)".format(d=d,
                                                                          kij=Kmesh[i][j],
                                                                          kijp1=Kmesh[i][j+1]))
                    else:
                        cEf.append(d / (0.5 * d / Kmesh[i][j + 1] + 0.5 * d / Kmesh[i][j]))
                    #if len(Smesh[i][j]) == 2:
                    #    cR.append(self.h_roof(Smesh[i][j], i, j))
                    #    lcR += 1
                    #else:
                    #    cR.append(0)
        self.lcR = lcR
        self.cf = c
        self.cNf = cNf
        self.cWf = cWf
        self.cSf = cSf
        self.cEf = cEf
        self.cRf = cR

    def h_roof(self, dirs, i, j):
        """Convection value for roof"""
        # The way the roof is setup is such that it has angle of 45 degrees always
        # Nu_e = 0.56(Gr_ePr_ecos(45))**0.25
        if dirs == 'NE':
            ii = i + No
            jj = j + Ea
        elif dirs == 'NW':
            ii = i + No
            jj = j + We
        elif dirs == 'SW':
            ii = i + So
            jj = j + We
        elif dirs == 'SE':
            ii = i + So
            jj = j + Ea
    def T_E(self, t=60*60*24*20, savestate=None, cvec=None):
        ttt = time.time()
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()


        Tmesh = self.Tmesh.copy()
        Tnew = self.Tnew.copy()

        # At the surfaces we have resistance due to convection and radiation of heat
        # There R = 1/(h_conv + h_rad), none surfaces do not have this factor
        c = self.c
        cS = self.cS
        cN = self.cN
        cE = self.cE
        cW = self.cW
        n = Tmesh.n
        mm = Tmesh.m
        str = ""

        if self.iii == 0:
            iii = int(math.ceil(t/self.dt))
        else:
            iii = self.iii
        cmdat = int(iii / 100)
        print("\n Total iterations: {}\tSave Rate: {}".format(iii, cmdat))
        if cmdat == 0:
            cmdat = 1
        const = self.const
        mesh = self.mesh
        sql = self.sql
        try:
            for ii in range(self.iis, iii):
                sys.stdout.write(
                    '\r STARTING CALCULATIONS FOR EXPLICIT METHOD...\t{}%\t{}\t{}'.format(round((ii + 1) * 100 / iii, 3),
                                                                                      time.time() - ttt, str))
                k = 0
                for i in range(n):
                    for j in range(mm):
                        if mesh[i][j] > 0:
                            Tnew[i][j] = Tmesh[i][j] + \
                                         (1 / c[k]) * \
                                         (cW[k] * (Tmesh[i][j - 1] - Tmesh[i][j]) +
                                          cE[k] * (Tmesh[i][j + 1] - Tmesh[i][j]) +
                                          cN[k] * (Tmesh[i - 1][j] - Tmesh[i][j]) +
                                          cS[k] * (Tmesh[i + 1][j] - Tmesh[i][j]))
                            k += 1
                if ii % cmdat == 0 or ii == 0 or ii == iii-1:
                    if ii == 0:
                        cmd = [i for i in Tmesh.A]
                    else:
                        cmd = [i for i in Tnew.A]
                    sql.insert_table(cursor, 'data', [ii, cmd])
                Tmesh = Tnew.copy()
        except KeyboardInterrupt:
            conn.commit()
            raise KeyboardInterrupt
        conn.commit()
        conn.close()
        sys.stdout.write('\r STARTING CALCULATIONS FOR EXPLICIT METHOD... DONE! {}\n'.format(time.time() - ttt))
        print(time.time() - ttt, t, self.dt, iii, self.mesh.size())
        return iii


    def which_T(self, i, j):
        return self.T[self.mesh[i][j]]

    def T_Ec(self, t=60*60*24):
        """
        FVM method including heat convection and radiation
        :param t: time
        :return: meshes
        """
        ttt = time.time()
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        Tmesh = self.Tmesh.copy()
        Tnew = self.Tnew.copy()

        # At the surfaces we have resistance due to convection and radiation of heat
        # There R = 1/(h_conv + h_rad), none surfaces do not have this factor

        c = self.cf
        cS = self.cSf
        cN = self.cNf
        cE = self.cEf
        cW = self.cWf
        n = Tmesh.n
        mm = Tmesh.m
        strr = ""
        Smesh = self.Smesh.copy()
        if self.iii == 0:
            iii = int(math.ceil(t / self.dt))
        else:
            iii = self.iii

        cmdat = int(iii / 100)      # interval at which data is committed c(o)m(mit)dat(a)
        if cmdat == 0: cmdat = 1
        print("\n Total iterations: {}\tSave Rate: {}".format(iii, cmdat))
        Pr = self.Pr
        nu = self.nu_air
        k_air  = self.k_air
        Tinf = self.Tinit.copy()
        which_T = self.which_T
        Rcalc = self.Rcalc
        const = self.const
        mesh = self.mesh
        sql = self.sql
        try:
            for ii in range(self.iis, iii):
                sys.stdout.write(
                    '\r STARTING CALCULATIONS FOR EXPLICIT METHOD...\t{}%\t{}\t{}'.format(round((ii + 1) * 100 / iii, 3),
                                                                                          time.time() - ttt, strr))
                k = 0
                for i in range(n):
                    for j in range(mm):
                        if mesh[i][j] > 0:
                            if isinstance(cW[k], str):
                                cWt = Rcalc(cW[k], i, j, 'W', Pr, nu, k_air, mm, which_T(i, j-1), Tmesh[i][j])
                            else:
                                cWt = cW[k]
                            if isinstance(cN[k], str):
                                cNt = Rcalc(cN[k], i, j, 'N', Pr, nu, k_air, mm, which_T(i - 1, j), Tmesh[i][j])
                            else:
                                cNt = cN[k]
                            if isinstance(cE[k], str):
                                cEt = Rcalc(cE[k], i, j, 'E', Pr, nu, k_air, mm, which_T(i, j+1), Tmesh[i][j])
                            else:
                                cEt = cE[k]
                            if isinstance(cS[k], str):
                                cSt = Rcalc(cS[k], i, j, 'S', Pr, nu, k_air, mm, which_T(i+1, j), Tmesh[i][j])
                            else:
                                cSt = cS[k]

                            Tnew[i][j] = Tmesh[i][j] + \
                                         (1 / c[k]) * \
                                         (cWt * (Tmesh[i][j - 1] - Tmesh[i][j]) +
                                          cEt * (Tmesh[i][j + 1] - Tmesh[i][j]) +
                                          cNt * (Tmesh[i - 1][j] - Tmesh[i][j]) +
                                          cSt * (Tmesh[i + 1][j] - Tmesh[i][j]))
                            #if isinstance(Tnew[i][j], complex):
                            #    Tnew[i][j] = Tnew[i][j].real
                            k += 1
                if ii % cmdat == 0 or ii == 0 or ii == iii-1:
                    if ii == 0:
                        cmd = [i for i in Tmesh.A]
                    else:
                        cmd = [i for i in Tnew.A]
                    sql.insert_table(cursor, 'data', [ii, cmd])
                    # conn.commit()
                Tmesh = Tnew.copy()
        except KeyboardInterrupt:
            conn.commit()
            raise KeyboardInterrupt
        conn.commit()
        conn.close()
        sys.stdout.write('\r STARTING CALCULATIONS FOR EXPLICIT METHOD... DONE! {}\n'.format(time.time() - ttt))
        print(time.time() - ttt, t, self.dt, iii, self.mesh.size())
        return iii

    def Rcalc(self, c, i, j, dir, Pr, nu, k, n, Tinf, Tw):
        """
        Calculates the conductive and radiative resistances at places where needed
        :param c: function
        :param i: index i, placement
        :param j: index j, placement
        :param dir: North, East, South or West
        :return: Value of c at location (i,j) in the mesh
        Page 265
        """
        #               1/2         -1/4    1/4
        # Nu_x = 0.508Pr   (0.952+Pr)   Gr_x
        # beta =approx= 1/T_gas
        # b = beta
        # x = length from bottom of wall ( (n-i)*dx )
        #        g*b(T_w-T_inf)       3
        # Gr_x = -------------------x
        #             nu^2
        #
        # h = Nu_x/(x*k_air)
        R = 0
        beta = 2/(Tinf+Tw)          # approximation
        ii = i
        jj = j
        if dir == 'N': ii -= 1
        elif dir == 'S': ii += 1
        elif dir == 'E': jj += 1
        elif dir == 'W': jj -= 1
        if self.Cmesh[ii][jj] > 5:
            return eval(c)      # this method is only for gasses, approximation: no gas has cp more than 5
        if 'E' in dir or 'W' in dir:
            Gr_x = 9.81*beta*abs(Tw-Tinf)/(nu**2)*((n-j)*self.d)**3
            Nu_x = 0.508*Pr**0.5*(0.952+Pr)**-0.25*Gr_x**0.25
            h = Nu_x/((n-j)*self.d*k)
            R += h

        else:
            mesh = self.mesh.copy()
            count = 1
            ii = i - 1
            vars = [mesh[i][j + 1], mesh[i][j], mesh[i][j - 1]]
            cont = True
            try:
                while cont:
                    if [mesh[ii][j + 1], mesh[ii][j], mesh[ii][j - 1]] == vars:
                        count += 1
                        ii -= 1
                    else:
                        cont = False
                        break
            except IndexError:
                pass
            ii = i + 1
            cont = True
            try:
                while cont:
                    if [mesh[ii][j + 1], mesh[ii][j], mesh[ii][j - 1]] == vars:
                        count += 1
                        ii += 1
                    else:
                        cont = False
                        break
            except IndexError:
                pass
            l = count * self.d
            if ('N' in dir and Tw > Tinf) or ('S' in dir and Tw < Tinf):
                h = 2*(abs(Tw-Tinf)/l)**0.25  # 1.32
            else:
                h = 1*(abs(Tw-Tinf)/l)**0.25  # 0.59
            R += h

        if R == 0:
            return eval(c)
        R = 1/R
        return eval(c)


    def str2mat(self, A):
        A = A[1:-1].replace('[', '')
        temp = []
        for each in A.split(']'):
            if each:
                if each[0] == ',':
                    each = each[2:]
                temp.append([float(i) for i in each.split(', ')])
        return matrix(temp)




if __name__ == "__main__":

    k = [20, 2.624 * 10 ** -1]
    ki = 0.02624
    ko = 0.02624
    kg = 1.5
    cp = [100, 100]
    cpi = 1.0057
    cpo = 1.0057
    cpg = 3000
    rho = [500, 7.706]
    rhoi = 1.1774
    rhoo = 1.1774
    rhog = 800
    # outside = 0, material =1, nomaterial, ground=last-1, last = air
    #      out   material ground in
    rho = [1.1774, 2400, 2200, 1.1774]
    k = [0.02624, 1.6, 1.3, 0.02624]
    cp = [1.0057, 900, 800, 1.0057]
    T = [273.15, 283.15, 278.15, 293.15]
    defaults = [T, rho, cp, k]
    const = [1, 0, 1, 1]
    house = House(1, 1, 7, 10, 10)
    house.add_floor()

    f = fvm(house.rmesh(), [float(i) for i in T],
            [float(i) for i in k],
            [float(i) for i in cp],
            [float(i) for i in rho], const, house.scale, "fvm_cond", house_class=house)
    f.k_air = k[0]
    f.Pr = 0.71
    f.nu_air = 15.69*10**-6
    f.T_Ec(t=60*60*24*5)
    conn, curs = f.sql.cc()
    data = f.sql.read_table(curs, 'data%s' % f.project)
    conn.close()
    for i in range(len(data)):
        data[i] = data[i][1]
    from engineer.FVM_temp.plotting import animation
    writer, ani = animation(data, f, name='Implicit', interval=50)
    name = 'animation%s.mp4' % f.project
    if os.path.exists(name):
        count = 1
        while os.path.exists(name):
            name = name.split('.')[0][:-1] + "%d.mp4" % count
            count += 1
    ani.save(name, writer=writer)
    print("\nVideo can be found in path:\n\t%s\n" % os.path.realpath(name))
