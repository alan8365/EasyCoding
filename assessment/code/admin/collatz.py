def collatz(number):
    count, maximum = 0, number
    while number != 1:
        count+=1
        if number % 2 == 0:
            number = number // 2
        else:
            number = number*3 + 1
            maximum=max(number,maximum)
    return (8, 16)