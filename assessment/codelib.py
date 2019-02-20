from random import randint, choice
from string import ascii_letters


def random_string_maker(length_range=(5, 15)):
    result = ""

    for _ in range(randint(*length_range)):
        result += choice(ascii_letters)

    return result


class Input_Range:
    """Base class for all input range"""

    def __init__(self, *args, input_type: type = None, input_range: tuple = None, **kwargs):
        self.input_type = input_type
        self.input_range = input_range

    def __iter__(self):
        result = (self.input_type, self.input_range)

        return iter(result)

    def __next__(self):
        pass

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "<Input_Range: %s range in %s>" % (self.input_type.__name__, self.input_range)


class Iterable_Input_Range_TEST(Input_Range):

    def __init__(self, length_range, **kwargs):
        super().__init__(**kwargs)
        self.length_range = length_range

    def __repr__(self):
        return "<Iterable_Input_Range: %s range in %s with length %s>" % (
            self.input_type.__name__, self.input_range, self.length_range)


class Iterable_Input_Range:

    def __init__(self, input_type, length_range, input_range):
        self.input_type = input_type
        self.input_range = input_range
        self.length_range = length_range


class Dict_Input_Range:

    def __init__(self, key_type, value_type, key_range, value_range, length_range):
        self.key_type = key_type
        self.value_type = value_type
        self.key_range = key_range
        self.value_range = value_range
        self.length_range = length_range


class Fixed_Key_Dict_Input_Range:

    def __init__(self, key_regular, value_type, value_range):
        self.key_regular = key_regular
        self.value_type = value_type
        self.value_range = value_range

        self.data = {
            key: value for key, value in zip(key_regular, zip(value_type, value_range))
        }


class Function_Data_Content:

    def __init__(self, function_name: str, function_input: str, input_type, input_range,
                 answer_function, sample_test: tuple,
                 is_bool=False):
        self.function_name = function_name
        self.function_input = function_input

        self.input_type = input_type
        self.input_range = input_range

        self.answer_function = answer_function
        self.sample_test = sample_test

        self.is_bool = is_bool

    def __str__(self):
        return self.function_name


# lesson 0

def hello_world():
    return "Hello world"


def isPrime(x):
    if x < 2:
        return False

    for i in range(2, x):
        if x % i == 0:
            return False

    return True


# lesson 2
def float_format(n1, n2, n3, n4):
    return '%8.2f%8.2f\n%8.2f%8.2f' % (n1, n2, n3, n4)


# lesson 3
def average(n1, n2, n3, n4):
    return (n1 + n2 + n3 + n4) / 4


def xnor(a, b):
    return not (a or b) or (a and b)


def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


# lesson 4

def median(score_list):
    score_list.sort()

    num = int(len(score_list) / 2)

    return (score_list[num] + score_list[num - 1]) / 2


str_sort_range = tuple(str(randint(256847, 54687658)) for i in range(50))


def str_sort(my_str):
    my_str = sorted(my_str, reverse=True)

    my_str = ''.join(my_str)

    return my_str


compare_suit_range = ('♠', '♥', '♦', '♣')


def compare_suit(suit1, suit2):
    poker_suit = {'♠': 4, '♥': 3, '♦': 2, '♣': 1}

    return poker_suit[suit1] > poker_suit[suit2]


def merge_tuple(tuple1, tuple2):
    tuple1 += tuple2

    return tuple(sorted(tuple1))


def repeat_elem(a):
    return len(set(a)) < len(a)


reverse_str_range = tuple(random_string_maker() for _ in range(50))


def reverse_str(my_str):
    return my_str[::-1]


# lesson 5
def bmi(weight, height):
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        return "過輕"
    elif bmi < 24:
        return "正常體重"
    elif bmi < 27:
        return "過重"
    else:
        return "肥胖"


def sd(tup):
    u = sum(tup) / len(tup)
    a = 0
    for i in tup:
        a += (i - u) ** 2
    return (a / len(tup)) ** 0.5


def collatz(number):
    count, maximum = 0, number
    while number != 1:
        if number % 2 == 0:
            number = number // 2
            count += 1
        else:
            number = number * 3 + 1
            count += 1
            maximum = max(number, maximum)
    return count, maximum


def mul_table(start, stop):
    a = ''
    for i in range(start, stop + 1):
        for j in range(start, stop + 1):
            a += str(i) + "*" + str(j) + '=' + str(i * j) + '\t'
        a += '\n'
    return a


def painting_stars(num):
    a = ''
    for i in range(num):
        for j in range(i):
            a += ' '
        for j in range(num - i):
            a += '*'
        a += '\n'
    for i in range(num - 1):
        for j in range(num - 1):
            a += ' '
        for j in range(i + 2):
            a += '*'
        a += '\n'
    return a


# lesson 6

knapsack_sample = (
    {"weight": 10, "price": 60},
    {"weight": 20, "price": 100},
    {"weight": 30, "price": 120}
)


def knapsack(load_weight, object_dict, **kwargs):
    if not kwargs:
        return knapsack(load_weight, object_dict, n=len(object_dict))

    n = kwargs["n"]

    if load_weight < 0:
        return float("-inf")

    if n == 0:
        return 0

    take_num = knapsack(
        load_weight=load_weight - object_dict[n - 1]["weight"],
        object_dict=object_dict,
        n=n - 1
    ) + object_dict[n - 1]["price"]

    do_not_take_num = knapsack(
        load_weight=load_weight,
        object_dict=object_dict,
        n=n - 1
    )

    return max(take_num, do_not_take_num)


function_data = {

    # lesson 0
    12: Function_Data_Content(
        function_name="hello_world",
        function_input="()",

        input_type=None,
        input_range=None,

        answer_function=hello_world,
        sample_test=((),),
    ),

    1: Function_Data_Content(
        function_name="isPrime",
        function_input="(x)",

        input_type=int,
        input_range=(10, 500),

        answer_function=isPrime,
        sample_test=(0, 1, 2, 3, 5, 6, 7, 9),

        is_bool=True
    ),

    # lesson 2
    2: Function_Data_Content(
        function_name="float_format",
        function_input="(n1, n2, n3, n4)",

        input_type=(float, float, float, float),
        input_range=((0, 200), (0, 200), (0, 200), (0, 200)),

        answer_function=float_format,
        sample_test=((24.102, 52.3, 62.124, 125.67),)
    ),

    # lesson 3
    3: Function_Data_Content(
        function_name="average",
        function_input="(n1, n2, n3, n4)",

        input_type=(float, float, float, float),
        input_range=((0, 200), (0, 200), (0, 200), (0, 200)),

        answer_function=average,
        sample_test=((47, 68, 91, 16),)
    ),

    23: Function_Data_Content(
        function_name="xnor",
        function_input="(a, b)",

        input_type=(bool, bool),
        input_range=((True, False), (True, False)),

        answer_function=xnor,
        sample_test=((False, False), (False, True), (True, False), (True, True),)
    ),

    15: Function_Data_Content(
        function_name="distance",
        function_input="(x1, y1, x2, y2)",

        input_type=(int, int, int, int),
        input_range=((-200, 200), (-200, 200), (-200, 200), (-200, 200)),

        answer_function=distance,
        sample_test=((2, -5, 6, -2),)
    ),

    # lesson 4
    26: Function_Data_Content(
        function_name="median",
        function_input="(score_list)",

        input_type=(list,),
        input_range=(
            Iterable_Input_Range(
                input_type=int,
                length_range=(10, 10),
                input_range=(-200, 200)
            ),
        ),

        answer_function=median,
        sample_test=(([58, 96, 100, 36, 54, 87, 95, 62, 34, 48],),)
    ),

    27: Function_Data_Content(
        function_name="str_sort",
        function_input="(my_str)",

        input_type=str,
        input_range=str_sort_range,

        answer_function=str_sort,
        sample_test=("13246574684",)
    ),

    28: Function_Data_Content(
        function_name="compare_suit",
        function_input="(suit1, suit2)",

        input_type=(str, str,),
        input_range=(compare_suit_range, compare_suit_range),

        answer_function=compare_suit,
        sample_test=(('♥', '♣'),)
    ),

    29: Function_Data_Content(
        function_name="merge_tuple",
        function_input="(tuple1, tuple2)",

        input_type=(tuple, tuple,),
        input_range=(
            Iterable_Input_Range(
                input_type=int,
                length_range=(2, 10),
                input_range=(-200, 200)
            ),
            Iterable_Input_Range(
                input_type=int,
                length_range=(2, 10),
                input_range=(-200, 200)
            ),
        ),

        answer_function=merge_tuple,
        sample_test=(((12, 56, 83, 22, 98, 51, 9), (64, 77, 89, 43, 21, 0, 99)),)
    ),

    30: Function_Data_Content(
        function_name="repeat_elem",
        function_input="(a)",

        input_type=(list,),
        input_range=(
            Iterable_Input_Range(
                input_type=int,
                length_range=(2, 30),
                input_range=(-20, 20)
            ),
        ),

        answer_function=repeat_elem,
        sample_test=(([25, 67, 88, 25, 33, 12],),)
    ),

    31: Function_Data_Content(
        function_name="reverse_str",
        function_input="(my_str)",

        input_type=str,
        input_range=reverse_str_range,

        answer_function=reverse_str,
        sample_test=("Python",)
    ),

    # lesson 5
    19: Function_Data_Content(
        function_name="sd",
        function_input="(tup)",

        input_type=(tuple,),
        input_range=(
            Iterable_Input_Range(
                input_type=int,
                length_range=(3, 6),
                input_range=(-200, 200)
            ),
        ),

        answer_function=sd,
        sample_test=(((5, 6, 8, 9),),)
    ),

    13: Function_Data_Content(
        function_name="bmi",
        function_input="(weight, height)",

        input_type=(int, int),
        input_range=((10, 110), (90, 220)),

        answer_function=bmi,
        sample_test=((57, 203),)
    ),

    20: Function_Data_Content(
        function_name="mul_table",
        function_input="(start, stop)",

        input_type=(int, int),
        input_range=((1, 6), (6, 9)),

        answer_function=mul_table,
        sample_test=((4, 6),)
    ),

    24: Function_Data_Content(
        function_name="collatz",
        function_input="(number)",

        input_type=int,
        input_range=(1, 100000000),

        answer_function=collatz,
        sample_test=(6, 6171,)
    ),

    25: Function_Data_Content(
        function_name="painting_stars",
        function_input="(num)",

        input_type=int,
        input_range=(1, 10),

        answer_function=painting_stars,
        sample_test=(4,)
    ),

    # lesson 6

    32: Function_Data_Content(
        function_name="knapsack",
        function_input="(load_weight, object_dict)",

        input_type=(int, tuple),
        input_range=(
            (30, 1000),
            Iterable_Input_Range(
                input_type=dict,
                length_range=(3, 10),
                input_range=Fixed_Key_Dict_Input_Range(
                    key_regular=("weight", "price"),
                    value_type=(int, int),
                    value_range=((0, 200), (0, 200))
                )
            ),
        ),

        answer_function=knapsack,
        sample_test=(
            (50, knapsack_sample),
        )
    )
}
