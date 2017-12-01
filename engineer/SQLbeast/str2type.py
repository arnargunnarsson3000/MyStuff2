import sys
import sqlite3
import os

__doc__ = """
<short>
DESCRIPTION: 

USAGE:
    str2type.py --option [--option2] [--varflag <var>] [--verbose] [--debug]
    str2type.py -h | --help
    str2type.py -v | --version

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

# functions to check if variable is of certain type
def isMat(arr):
    """
    Checks to see if arr is a matrix, matric must of same form as in my engineer.linear package
    :param arr: input argument, string format
    :return: True or False
    """
    if arr[:2] == "[[":
        return True
    return False

def isFloatArr(arr):
    try:
        temp = str2floatArr(arr)
    except ValueError:
        return False
    if len(temp) > 1:
        return True
    return False

def isIntArr(arr):
    if isFloatArr(arr):
        temp = str2floatArr(arr)
        if max([float(i)-int(i) for i in temp]) < 0.0001:
            return True
        else:
            return False
    else:
        return False

def isStrArr(arr):
    try:
        if isFloatArr(arr):
            return False
    except ValueError:
        pass
    if isinstance(arr, list):
        for each in arr:
            if not isinstance(each, str):
                return False
    elif isinstance(arr, str):
        if arr.replace("[", '').replace("]", '') == arr:
            temp = arr.split(', ')
            for each in temp:
                if not isinstance(each, str):
                    return False
        else:
            temp = arr.replace("[", '').replace("]", '').split(', ')
            for each in temp:
                if not isinstance(each, str):
                    return False
    return True

def isArr(arr):
    """
    Checks if this str arr is an array
    :param arr:
    :return:
    """
    return not arr.replace('[','') == arr

def isFloat(arr):
    """
    Checks if input is float
    :param arr: input argument
    :return: True or False
    """
    try:
        temp = float(arr)
    except (TypeError, ValueError):
        return False
    return True

def isDict(arr):
    """
    Checks to see if input string arr is a dictionary
    :param arr:
    :return: True/False
    """
    temp = {}
    if not isinstance(arr, str):
        return False
    try:
        for key_val in arr.split("||"):
            temp[key_val.split("|")[0]] = key_val.split("|")[1]
    except IndexError:
        return False
    return True

# functions that change a string to its respective type
def str2arr(arr):
    if isIntArr(arr):
        return str2intArr(arr)
    elif isFloatArr(arr):
        return str2floatArr(arr)
    elif isStrArr(arr):
        return arr  #TODO

def str2mat(A):
    A = A[1:-1].replace('[', '')
    temp = []
    for each in A.split(']'):
        if each:
            if each[0] == ',':
                each = each[2:]
            temp.append([float(i) for i in each.split(', ')])
    return temp

def str2floatArr(arr):
    """
    Input arr can be either string of array or array of string: e.g.
        arr = "[<value1>, <value2>, <value3>]"
            Attempts to split arr and isolate the <values> and then trys to float(<value_i>)
        OR
        arr = ["<value1>", "<value2>", "<value3>"]
            Attempts to float("<value_i>") for all i
    :param arr:
    :return:
    """
    if isinstance(arr, str):
        arr = arr.replace("[",'').replace("]",'')
        arr = arr.split(", ")
    for i in range(len(arr)):
        pow = 1.0
        mult = 1.0
        mid = 1.0
        if isinstance(arr[i].split('**'), list) and len(arr[i].split('**')) > 1:
            pow = float(arr[i].split('**')[-1])
            arr[i] = arr[i].replace('**'+arr[i].split('**')[-1], '')
        if isinstance(arr[i].split('*'), list) and len(arr[i].split('*')) > 1:
            mult = float(arr[i].split('*')[0])
            mid = float(arr[i].split('*')[-1])
        else:
            mid = float(arr[i])
        arr[i] = mult*mid**pow
    return arr

def str2intArr(arr):
    """
           Input arr can be either string of array or array of string: e.g.
               arr = "[<value1>, <value2>, <value3>]"
                   Attempts to split arr and isolate the <values> and then trys to int(<value_i>)
               OR
               arr = ["<value1>", "<value2>", "<value3>"]
                   Attempts to int("<value_i>") for all i
           :param arr:
           :return:
           """
    if isinstance(arr, str):
        arr = arr.replace("[", '').replace("]", '')
        arr = arr.split(", ")
    for i in range(len(arr)):
        pow = 1.0
        mult = 1.0
        mid = 1.0
        if isinstance(arr[i].split('**'), list) and len(arr[i].split('**')) > 1:
            pow = float(arr[i].split('**')[-1])
            arr[i] = arr[i].replace('**' + arr[i].split('**')[-1], '')
        if isinstance(arr[i].split('*'), list) and len(arr[i].split('*')) > 1:
            mult = float(arr[i].split('*')[0])
            mid = float(arr[i].split('*')[-1])
        else:
            mid = float(arr[i])
        arr[i] = int(mult * mid ** pow)
    return arr

def str2strArr(arr):
    """
           Input arr can be either string of array or array of string: e.g.
               arr = "[<value1>, <value2>, <value3>]"
                   Attempts to split arr and isolate the <values> and then trys to isolate and attempts to
                   return ["<value1>", "<value2>", "<value3>"]
               OR
               arr = ["<value1>", "<value2>", "<value3>"]
                   Attempts to
                   return ["<value1>", "<value2>", "<value3>"]
           :param arr:
           :return:
           """
    if isinstance(arr, str):
        temp1 = arr.replace("[", '').replace("]", '')
        temp1 = temp1.split(", ")
        temp = []
        for i in range(len(temp1)):
            temp.append(temp1[i])
        if len(temp) == 1:
            temp = temp[0]
        return temp
    return arr

def str2float(arr):
    return float(arr)


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

def str2dict(arr):
    """
    Parses a string into a dictionary, if correct format
    :param arr: input string
    :return: dictionary of input string
    """
    temp = {}
    for key_val in arr.split("||"):
        temp[key_val.split("|")[0]] = key_val.split("|")[1]
    return temp

# automatic string to values for list or single input
def str2val(arr):
    if isDict(arr):
        return str2dict(arr)
    if isMat(arr):
        return str2mat(arr)
    if isIntArr(arr):
        return str2intArr(arr)
    if isFloat(arr):
        return str2float(arr)
    if isFloatArr(arr):
        return str2floatArr(arr)
    if isStrArr(arr):
        return str2strArr(arr)
    return arr

def arr2val(arr):
    data = []
    for each in arr:
        data.append(str2val(each))
    return data



if __name__ == "__main__":
    a = [1,2,3,4,5]
    b = str(a)
    c = [1.2345*i for i in a]
    d = str(c)
    a = ['a','b','c','d']
    c = str(a)
    print(c, str2arr(c), type(c[0]), 'str')
    print(a, str2arr(a), type(a[0]), 'str')
    print(b, str2arr(b), type(str2arr(b)[0]), 'int')
    print(d, str2arr(d), type(str2arr(d)[0]), 'float')
