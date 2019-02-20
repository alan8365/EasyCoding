def mul_table(start, stop):
    a=''
    for i in range(start,stop+1):
        for j in range(start,stop+1):
            a += str(i) + "*" + str(j) + '=' + str(i*j) + '\t'
        a+='\n'
    return a