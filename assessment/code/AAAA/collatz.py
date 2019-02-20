def collatz(number):
    a,b=0,number
    while number!=1:
        number = number//2 if number%2 == 0 else number*3+1;b=max(number,b)
        a+=1
    return a,b