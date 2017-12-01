import sqlite3
import engineer.SQLbeast.sql_class as sql_class
import engineer.SQLbeast.str2type as str2type
import os, sys
from engineer.Algebra.linear import matrix


if __name__ == "__main__":
    db_name = "Test_DB.db"
    a = sql_class.load(db_name, "addi2")
    conn, curs = a.cc()
    try:
        a.create_table(curs, 'teststuff2', ['nums'])
    except sqlite3.OperationalError:
        a.insert_table(curs, 'teststuff2', '1')
        a.save_status(curs)
    a.ccc(conn)
    exit(0)
    if not os.path.exists(db_name):
        sql_class.create_db(db_name)

    sq_handler = sql_class.sql_cmds(db_name,)
    conn = sqlite3.connect(db_name)
    curs = conn.cursor()

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
    os.remove(db_name)
