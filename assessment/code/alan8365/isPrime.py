def isPrime(x):
    if x < 2:
        return False

    for i in range(2, x):
        if x % i == 0:
            break
    else:
        return True

