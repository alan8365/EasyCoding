def isP(x):
    for i in range(2,x):
        if x % i == 0:
            return False
    return True

test = input()

print(isP(int(test)))