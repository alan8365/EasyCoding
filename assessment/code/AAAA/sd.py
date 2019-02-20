def sd(tup):
    u=sum(tup)/len(tup)
    a=0
    for i in tup:
        a+=(i-u)**2
    return (a/len(tup))**0.5