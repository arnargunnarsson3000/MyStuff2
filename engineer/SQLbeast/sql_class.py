import os, sys
import sqlite3
import engineer.SQLbeast.str2type as str2type
import engineer.SQLbeast.type2str as type2str
from engineer.SQLbeast.basic_usefull.type_handling import Misinstance
from engineer.SQLbeast.DEFAULT_SQL_COMMANDS import CREATE_DB, DOES_TABLE_EXIST, CREATE_TABLE, INSERT_TABLE, DELETE_TABLE, DROP_TABLE, READ_TABLE, LIST_TABLES

__doc__ =  """
<short>
DESCRIPTION: 

USAGE:
    sql_class.py --option [--option2] [--varflag <var>] [--verbose] [--debug]
    sql_class.py -h | --help
    sql_class.py -v | --version

OPTIONS:
    -h, --help       Shows this help and exits
    -v, --version    Print tool version and exits
    --verbose        Run with lots of information
    --debug          Run in debug mode

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Author:		Arnar Evgeni Gunnarsson
Date:		2017-11-15
Version:	dev
Contact:	s171950@student.dtu.dk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Danmarks Tekniske Universitet
	Engineering Design & Applied Mechanics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Development of Engineering Tools
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""


class sql_cmds:
    """
    A class for creating and hadnling an SQL database.
    Default tables are (columns as well and descriptions):
    -<project>
        |name|
    -<SessionSave/sess>:    Last row contains the same as <lastsave> but also table dictionary
        |name|dictionary|
    -<lastsave>:    Last row is the name of last project, updates in save_status
        |savepoint|
    -<allsave>
        |name|data|
    -<init>:        Contains only 1 row with 1, to check if project is initialized
        |1|
    -<handler>
        |name|vars|length|
    """
    def __init__(self, db, project=None):
        self.db = db
        if not os.path.exists(db):
            create_db(db)
        if project:
            self.project = project

            self.lastsave = "lastsave"
            self.allsave = "allsave%s" % project
            self.handler = "handler%s" % project
            self.init = "init%s" % project
            self.sess = "SessionSave%s" % project
            self.dic = {
                self.sess: 2,
                self.init: 1,
                self.handler: 3,
                self.allsave: 2,
                self.lastsave: 1
            }
            self.tables = []
            for key, item in self.dic.items():
                self.tables.append(key)
            conn = sqlite3.connect(self.db)
            curs = conn.cursor()
            if not self.isInit(curs):
                print("not inited")
                self.init_db(conn, curs)
            self.save_status(curs)
            conn.commit()
            conn.close()
        else:
            self.project = False

    def isInit(self, curs):
        """
        Checks to see if project has been initialized
        :param curs: database connection cursor
        :return: True if project has been initialized
        """
        if self.table_exist(curs, self.init):
            return True
        return False

    def init_db(self, conn, curs):
        """
        Initializes database
        :param conn: database connector
        :param curs: connector's cursor
        :return: 0 if successful
        """
        self.create_table(curs, self.project, 'name')
        if not self.table_exist(curs, 'lastsave'):
            self.create_table(curs, self.lastsave, 'savepoint')
        self.create_table(curs, self.sess, ['db_name', 'diction'])
        self.create_table(curs, self.allsave, ['name', 'data'])
        self.create_table(curs, self.handler, ['name', 'vars', 'length'])
        self.create_table(curs, self.init, 'started')
        self.insert_table(curs, self.init, '1')
        conn.commit()
        return 0

    def read_table(self, curs, name):
        """
        Reads all data from a table, list of tables is also possible.
        All rows in table are appended and returned.
        The output is:
            [[(),(),...],[(),(),...],...]
            list of lists, tuple is inside that
            output[i] returns all data of table at index i of name (name can be list, if not list, still do this)
            output[i][j] return data in form of tuple of table i row j
            output[i][j][k] return data in form string table i row j column k
        :param curs: the connection cursor
        :param name: name(s) of tables you want to read
        :param db: the name of the database if one is not given then the default of the class is used/hopefully set
        :return: all data from the tables that you wanted to read if you didn't make any mistakes that is
        """
        try:
            return READ_TABLE(name+self.project, curs=curs)
        except sqlite3.OperationalError:
            return READ_TABLE(name, curs=curs)

    def delete_table(self, curs, name):
        """
        Clear table of all stored data, doesn't actually delete the table like the name
        would indicate, SQL is weird like that
        :param curs: the connection cursor
        :param name: name(s) of tables you want to read
        :return: yes/no if table was cleared
        """
        DELETE_TABLE(name, curs=curs)
        return 0

    def drop_table(self, curs, name):
        """
        Drops table/deletes table COMPLETELY
        :param curs: database connection cursor
        :param name: table name to be dropped
        :return:
        """
        DROP_TABLE(name, curs=curs)
        return 0

    def create_table(self, curs, name, vars, types=None, overwrite=False):
        """
        Creates a table in database
        :param curs: database connection cursor
        :param name: name of table to be created
        :param vars: variables in table, should be an list of strings that hold column names ex: ['names', 'matrix']
        :param types: OPTIONAL, string holding types of each column, in same order is 'vars' ex: ['str', 'matrix']
        :return: 0 if creation successful
        """
        if not isinstance(vars, list):
            vars = [vars]
        if self.project:
            if self.project not in name and name != "lastsave" and name != self.project:
                name = name+self.project
        CREATE_TABLE(name, vars, curs=curs, overwrite=overwrite)
        if self.project:
            self.insert_table(curs, self.project, name)
        return 0

    def insert_table(self, curs, name, vars):
        """
        Insert data into table.
        :param curs: database connection cursor
        :param name: name of table to insert data into
        :param vars: LIST of information that is inputted, length should be the same as column length of table
        can be string or native type, if native it will be turned into a string
        :return: 0 if successful
        """
        try:
            INSERT_TABLE(name+self.project, vars, curs=curs)
        except sqlite3.OperationalError:
            try:
                INSERT_TABLE(name, vars, curs=curs)
            except sqlite3.OperationalError:
                INSERT_TABLE(name + self.project, vars, curs=curs)
        return 0

    def table_exist(self, curs, name):
        """
        Checks if a single table exists in a database
        :param curs: connection cursor
        :param name: name of a table
        :return: True False
        """
        return DOES_TABLE_EXIST(name, curs=curs)

    def cc(self):
        """
        returns connection and cursor to database
        """
        conn = sqlite3.connect(self.db)
        curs = conn.cursor()
        return conn, curs

    def ccc(self, conn):
        """
        Commits and closes a database connection
        :param conn: connector to database
        :return: 0 if everything successful
        """
        conn.commit()
        conn.close()
        return 0

    def save_status(self, curs):
        """
        Saves current settings/variables of THIS class
        :param curs: cursor to database connection
        :return: 0 if successful
        """
        dicti = type2str.val2str(self.dic)
        self.insert_table(curs, self.sess, [self.project, dicti])
        self.insert_table(curs, self.lastsave, self.project)

    def list_tables(self, curs):
        """
        lists tables, their names
        :param curs:
        :return:
        """
        return LIST_TABLES(curs=curs)


def create_db(name):
    """
    Creats a database.
    :param name: Name of database
    :return: True if creation successful
    """
    CREATE_DB(name)
    return 0


def delete_db(name):
    try:
        os.remove(name)
        return 0
    except FileNotFoundError:
        raise SystemError("No such file or directory bruv, try again...")


def load(db, project=None):
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    if project:
        a = sql_cmds(db, project=project)
        data = a.read_table(curs, a.sess)
        print(str2type.str2dict(data[0][-1][1]))

        # a.dic = str2type.str2dict(data[-1][])
    conn.commit()
    conn.close()
    return a



if __name__ == "__main__":
    pass