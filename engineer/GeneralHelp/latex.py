from engineer.Algebra.linear import matrix

def isnum(num):
    try:
        float(num)
        return True
    except ValueError:
        pass
    try:
        int(num)
        return True
    except ValueError:
        pass
    return False

DICT = dict([
            ['th','\\theta'],
            ['al','\\alpha']
            ])

def Lmatrix(A, num=None):
    str = "\\begin{equation}\nA_{i}=\n{\\small\n\\left[\\begin{array}{"
    str += "c"*A.n + "}"
    for i in range(A.n):
        for j in range(A.m):
            str += "{}".format(A[i][j])
            if j == A.m-1:
                str += " \\\\\n"
            else:
                str += " & "
    str += "\\end{array}\\right]\n}\n\\end{equation}"
    str = str.replace('cos','\cos').replace('sin','\sin')
    str = str.replace('(','\left(').replace(')','\\right)')
    if num:
        for m in num:
            i = 0
            while i != len(str):
                if str[i:i+len(m)] == m:
                    if isnum(str[i+len(m)]):
                        #print(str[:i])
                        #print(str[i+len(m)])
                        #print(str[i+len(m)+1:])
                        temp = ""
                        try:
                            temp = DICT[m]
                        except KeyError:
                            temp = str[i:i+len(m)]
                        str = str[:i] + temp + '_{' + '{}'.format(str[i+len(m)]) + '}' + str[i+len(m)+1:]
                i += 1
    str = str.replace('*','')
    return str

def Lcases(A):
    str = "\\begin{equation}\n\\begin{cases}\n"
    for each in A:
        str += " {}\\\\\n".format(each)
    str += "\\end{cases}\n\\end{equation}\n"
    return str

if __name__ == "__main__":
    print(isnum('a'))
    print(isnum('1.0'))
    I = matrix(4)
    print(I)
    Lmatrix(I)