def power(a, x):
    if x == 0:
        return a

    ans = 1

    for i in range(x):
        ans *= a

    return ans

