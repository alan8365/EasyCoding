def pokers_num(s1, s2, s3, s4, s5):
    my_dict = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
               'K': 13}
    return my_dict[s1] + my_dict[s2] + my_dict[s3] + my_dict[s4] + my_dict[s5]