import sys
import sqlite3
import os

__doc__ = """
<short>
DESCRIPTION: 

USAGE:
    type2str.py --option [--option2] [--varflag <var>] [--verbose] [--debug]
    type2str.py -h | --help
    type2str.py -v | --version

OPTIONS:
    -h, --help       Shows this help and exits
    -v, --version    Print tool version and exits
    --verbose        Run with lots of information
    --debug          Run in debug mode

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Author:		Arnar Evgeni Gunnarsson
Date:		2017-11-19
Version:	dev
Contact:	s171950@student.dtu.dk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Danmarks Tekniske Universitet
	Engineering Design & Applied Mechanics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Development of Engineering Tools
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""

# functions that change types to strings
def mat2str(A):
    """
    Turns matrix into string, format of which is allowable with these packages
    :param A: matrix
    :return: string of matrix
    """
    return str(A.A)

def arr2str(arr):
    """
    Turns list into string
    Allowable list types:
        ints
        floats
        string
    REMEMBER TO ADD TYPES IF TO DOC STRING IF CHANGED
    :param arr: list of type above
    :return: string of input array
    """
    if isinstance(arr[0], int) or isinstance(arr[0], float):
        return str(arr)
    print(arr)
    return "'[%s]'" % ", ".join(arr)


# automatic string to values for list or single input
def val2str(arr):
    """
    Automatically turns input argument into legal insert for SQL
    Current allowable types:
        Matrix:
            -ints
            -floats
            -strings
        ints
        floats
        string
        list
            -ints
            -floats
            -strings
        dictionary
    :param arr:
    :return:
    """

    # list, matrix
    if isinstance(arr, list):
        if isinstance(arr[0], list):
            # matrix
            if isinstance(arr[0][0], str):
                # string matrix
                temp = []
                for row in arr:
                    temp.append("[%s]" % ", ".join(row))
                return "'[%s]'" % ", ".join(temp)
            else:
                # float or int matrix
                return "'%s'" % str(arr)
        else:
            # normal list
            if isinstance(arr[0], str):
                # list of strings
                return "'[%s]'" % ", ".join(arr)
            else:
                # list of floats or ints
                return "'%s'" % str(arr)
    # Dictionary
    if isinstance(arr, dict):
        to_str = []
        for key, item in arr.items():
            to_str.append("%s|%s" % (key, item))
        return "%s" % "||".join(to_str)
    else:
        return "'%s'" % arr

def table_in2str(arr):
    """
    MAIN FUNCION TO USE TO TURN CONVERT TO SQL FORMAT
    :param arr:
    :return:
    """
    if not isinstance(arr, list):
        arr = [arr]
    data = []
    for each in arr:
        data.append(val2str(each))
    return ", ".join(data)

def arr2val(arr):
    data = []
    for each in arr:
        data.append(val2str(each))
    return data


if __name__ == "__main__":
    a = [1,2,3,4,5]
    b = str(a)
    c = [1.2345*i for i in a]
    d = str(c)
    a = ['a','b','c','d']

