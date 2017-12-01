import sqlite3
import engineer.SQLbeast.sql_class as sql_class
import engineer.SQLbeast.str2type as str2type
import engineer.SQLbeast.type2str as type2str
import os, sys
from engineer.Algebra.linear import matrix
from math import sin, cos
from engineer.SQLbeast.DEFAULT_SQL_COMMANDS import *


def create_random_values_in_db(db, conn, curs):

    a = sql_class.sql_cmds(db, project='test_shit')
    A = matrix(100, 100)
    for i in range(A.n):
        for j in range(A.m):
            A[i][j] = 10*sin(i) + 20*cos(j) + 10*3**cos(i*j)
    count = 1
    for row in A.A:
        a.create_table(curs, "table_number%s"%count, ['ival{}'.format(i+1) for i in range(A.m)])
        for i in range(len(row)):
            a.insert_table(curs, "table_number%s"%count, [j for j in row])
        count += 1

def work_with_random_values_in_db(db, conn, curs):
    data = LIST_TABLES(curs=curs)
    for each in data:
        print(each)

if __name__ == "__main__":

    db_name = "Test_DB.db"
    # if os.path.exists(db_name): os.remove(db_name)
    # CREATE_DB(db_name)
    conn = sqlite3.connect(db_name)
    curs = conn.cursor()
    # create_random_values_in_db(db_name, conn, curs)

    work_with_random_values_in_db(db_name, conn, curs)


    conn.commit()
    conn.close()
    exit(0)



    sq_handler.create_table(curs, 'test_table', ['str', 'list', 'matrix', 'dictionary'], overwrite=True)      # works with and without overwrite
    istr = ["this is a test string"]*5
    idict = {'a':1, 'b':2, 'c':3}
    ilist = [1,2,3,4,5]
    imat = [[1,2,3],[1,2,3]]
    sq_handler.insert_table(curs, 'test_table', [istr, ilist, imat, idict])
    sq_handler.insert_table(curs, 'test_table', [istr, ilist, imat, idict])
    sq_handler.insert_table(curs, 'test_table', [istr, ilist, imat, idict])
    data = sq_handler.read_table(curs, 'test_table')
    for row in data[0]:
        temp = []
        for each in str2type.arr2val(row):
            print(each)
            temp.append(each)
    sstr = "0123456789"
    ints = temp[1]
    for i in ints:
        print(sstr[i], i)
    conn.close()
