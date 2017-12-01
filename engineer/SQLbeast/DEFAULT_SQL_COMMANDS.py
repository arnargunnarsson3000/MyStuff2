import sqlite3
import os, sys
import configparser
from engineer.DefaultSettings.get_default_settings_path import default_settings_db_path
import engineer.SQLbeast.type2str as t2s
import engineer.SQLbeast.str2type as s2t

cfg = configparser.ConfigParser()
cfg.read(default_settings_db_path())                            # Default configuration


def CREATE_DB(name, overwrite=True, **kwargs):
    """
    Creates database after Arnar's standards, includes table <Default-Table-Handler-Name>
    :param name: name of database
    :return: nothing
    """
    if os.path.exists(name):                                # Deletes database if it exists
        if overwrite:
            print("Database exists, removing and creating new one!")
            os.remove(name)
        else:
            print("PickyBitchError: Overwrite set to False and database exists\nWhat do you want me to do?\n\nLearn better")
            exit(1)

    conn = sqlite3.connect(name)                                    # Created & connects to database
    curs = conn.cursor()                                            # Cursor to databse in previous line
    table_handler_name = cfg.get("TABLE_HANDLER", "name")           # name of table that holds all table names and information
    cols = s2t.str2val(cfg.get("TABLE_HANDLER", "cols"))            # the columns of table in previous line
    CREATE_TABLE(table_handler_name, cols, conn=conn, curs=curs)    # Creates table that stores table information


def DOES_TABLE_EXIST(name, **kwargs):
    """
    Check to see whether a table exists in a database
    Options:
        db=<database_name>
        conn=<connection_to_database>
        curs=<connection_cursor>
        verbose=<quite_or_loud>     Default False
    :param kwargs:
    :return:
    """
    conn, curs = return_conn_curs_after_kwargs(kwargs)
    try:
        curs.execute("SELECT * FROM %s" % name)
        return True
    except sqlite3.OperationalError:
        return False


def CREATE_TABLE(name, vars, **kwargs):
    """
    Options:
        db=<database_name>
        conn=<connection_to_database>
        curs=<connection_cursor>
        commit=<commit_once_done>   Default True, cannot commit if only curs provided
        verbose=<quite_or_loud>     Default False
        overwrite=<overwrite_table_if_exist>    Default False

    :param kwargs: options
    :return: 0=success, 1=table_exist&overwrite false
    """
    commit = to_commit_or_not_to_commit(True, kwargs)
    conn, curs = return_conn_curs_after_kwargs(kwargs)
    if DOES_TABLE_EXIST(name, curs=curs):
        # print("Table %s already exists" % name)
        if "overwrite" in kwargs:
            if kwargs["overwrite"]:
                DROP_TABLE(name, conn=conn, curs=curs)
            else:
                print("table deleted", name)
                DELETE_TABLE(name, curs=curs)
        else:
            print("table deleted", name)
            DELETE_TABLE(name, conn=conn, curs=curs)
    if not DOES_TABLE_EXIST(name, curs=curs):
        curs.execute("CREATE TABLE %s\n\t(%s)"% (name, ", ".join(vars)))
        ADD_TO_TABLE_DICT(name, vars, conn, curs, kwargs)
    if commit and conn:
        conn.commit()
    should_i_close_now(conn, kwargs)
    return 0


def INSERT_TABLE(name, vars, **kwargs):
    """
    Insert values into a table
    :param name:
    :param vars:
    :param kwargs:
    :return:
    """
    conn = None
    commit = to_commit_or_not_to_commit(False, kwargs)      # Default set to False since many insertion may done in a short amount of time
    conn, curs = return_conn_curs_after_kwargs(kwargs)

    #try:
    curs.execute("INSERT INTO %s VALUES (%s)" % (name, t2s.table_in2str(vars)))
    #except sqlite3.OperationalError:
    #    print("INSERT INTO %s VALUES (%s)" % (name, t2s.table_in2str(vars)))
    #    curs.execute("INSERT INTO %s VALUES (%s)" % (name, t2s.table_in2str(vars)))
    if commit and conn:
        conn.commit()
    should_i_close_now(conn, kwargs)


def DELETE_TABLE(name, **kwargs):
    """
    Clears all data from a given table
    :param name: name of table to clear
    :param kwargs: options !!!!TODO!!!!
    :return:
    """
    conn, curs = return_conn_curs_after_kwargs(kwargs)
    commit = to_commit_or_not_to_commit(True, kwargs)
    curs.execute("DELETE FROM %s" % name)
    if commit and conn:
        conn.commit()
    should_i_close_now(conn, kwargs)


def DROP_TABLE(name, **kwargs):
    """
    Deletes the table, all memory of it gone, never to be found again :^P
    :param name: name of table
    :param kwargs: options
    :return:
    """
    conn, curs = return_conn_curs_after_kwargs(kwargs)
    commit = to_commit_or_not_to_commit(True, kwargs)
    curs.execute("DROP TABLE %s" % name)
    if commit:
        conn.commit()
    REMOVE_FROM_TABLE_DICT(name, conn, curs, kwargs)
    should_i_close_now(conn, kwargs)


def READ_TABLE(name, **kwargs):
    """
    Reads a table, db, conn, curs depends on kwargs
    :param name:
    :param kwargs:
    :return:
    """
    conn, curs = return_conn_curs_after_kwargs(kwargs)
    table_data = []
    for row in curs.execute("SELECT * FROM %s" % name):
        table_data.append(row)
    return table_data


def LIST_TABLES(**kwargs):
    """
    Lists all tables in database
    :param kwargs: options
    :return:
    """
    conn, curs = return_conn_curs_after_kwargs(kwargs)
    return READ_TABLE(cfg.get("TABLE_HANDLER", "name"), curs=curs)


# Private functions, should not be used outside this script
def ADD_TO_TABLE_DICT(name, vars, conn, curs, kwargs):
    """
    This function should only be used automatically by this script
    Using it outside will complicate things.
    Updates to table handler after args, should match the config file being used
    :return:
    """
    if not isinstance(vars, list):
        vars = [vars]               # vars should be a list ALWAYS, just to see the amount of variables
    table_handler_name = cfg.get("TABLE_HANDLER", "name")
    INSERT_TABLE(table_handler_name, [name, str(len(vars))], conn=conn, curs=curs, commit=True)


def REMOVE_FROM_TABLE_DICT(name, conn, curs, kwargs):
    """
    This function should only be used automatically by this script
    Using it outside will complicate things.
    If a table gets deleted then it is removed from the database table handler
    :param name: name of table
    :param conn: connection to database
    :param curs: connection cursor
    :param kwargs: options
    :return:
    """
    table_handler_name = cfg.get("TABLE_HANDLER", "name")
    colname = s2t.str2val(cfg.get("TABLE_HANDLER", "cols"))[0]
    curs.execute("DELETE FROM %s where %s = '%s'" % (table_handler_name, colname, name))
    conn.commit()


def return_conn_curs_after_kwargs(kwargs):
    """
    Based on the input variables, returns connection to database and cursor
    :param kwargs:
    :return:
    """
    conn = None
    curs = None
    if "db" not in kwargs and "curs" not in kwargs and "conn" not in kwargs and "Pass" not in kwargs:
        print("\n".join(["OpSecError: not enough information given",
                        "\tMust give one of the following",
                        "\t\tdb=<databasename>",
                        "\t\tconn=<database_connector>",
                        "\t\tcurs=<connection_cursor>"]))
        raise
    if "db" in kwargs:
        conn = sqlite3.connect(kwargs["db"])
        curs = conn.cursor()
    if "conn" in kwargs:
        if kwargs["conn"]:
            conn = kwargs["conn"]
            curs = conn.cursor()
    if "curs" in kwargs:
        curs = kwargs["curs"]

    return conn, curs


def to_commit_or_not_to_commit(default, kwargs):
    """
    Based on kwargs and defaults for committing, returns True/False
    for committing after table insertion and table creation
    Default:
        table creation True
        table insertion False
    :param kwargs:
    :return:
    """
    if "commit" in kwargs:
        return kwargs["commit"]
    return default


def should_i_close_now(conn, kwargs, CnC=False):
    """
    Depending on kwargs, decides whether or not to close connection to database
    Always commits before closing. Unless CnC (close no commit) is set to True
    :param conn:
    :param kwargs:
    :return:
    """
    if "conn" not in kwargs:        # if conn is not in kwargs, then it was opened locally and must be closed
        if not CnC and conn:
            conn.commit()
        if conn:
            conn.close()


if __name__ == "__main__":

    # print(cfg_parser.sections())
    # print(cfg_parser.get("TABLE_HANDLER", "name"))
    # print(type(cfg_parser.get("TABLE_HANDLER", "name")))
    CREATE_DB("Test.db")
    CREATE_TABLE("name_here", ["vars", "go", "here"], db="Test.db", commit=False)
    print(READ_TABLE(cfg.get("TABLE_HANDLER", "name"), db="Test.db"))
    DROP_TABLE("name_here", db="Test.db", commit=False)
    print(READ_TABLE(cfg.get("TABLE_HANDLER", "name"), db="Test.db"))
    os.remove("Test.db")




