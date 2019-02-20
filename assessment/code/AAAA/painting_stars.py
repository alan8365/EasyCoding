def painting_stars(num):
    a=''
    for i in range(num):
        for j in range(i):
            a+=' '
        for j in range(num-i):
            a+='*'
        a+='\n'
    for i in range(num-1):
        for j in range(num-1):
            a+=' '
        for j in range(i+2):
            a+='*'
        a+='\n'
    return a