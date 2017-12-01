

def Misinstance(*args):
    """
    Small function, first input argument is a variable to check and the rest of them are types
    that you want to check if variable is.
    :param args: look above brrr
    :return: Types, python is cool like that if variable isn't empty then it is true, wow, look at that
    """
    var = args[0]
    types = args[1:]
    which = []
    for each in types:
        if isinstance(var, each):
            which.append(each)

    return which