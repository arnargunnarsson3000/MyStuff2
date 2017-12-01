

def linspace(start, stop, n, istart=True, istop=True):
    """
    linearly space over an interval
    :param start: starting point
    :param stop: stopping point
    :param n: number of elements
    :param istart: include start point
    :param istop: include end point
    :return: linearly spaced array
    """
    n = n-1
    arr = [start  + ((stop-start)/n) * i for i in range(n+1)]
    return arr


if __name__ == "__main__":
    linspace(2, 10, 4)
    linspace(3, 10, 5)