class Function_Data_Content:

    def __init__(self, function_name, function_input, input_type, input_range, answer_function, sample_test,
                 is_bool=False):
        self.function_name = function_name
        self.function_input = function_input

        self.input_type = input_type
        self.input_range = input_range

        self.answer_function = answer_function
        self.sample_test = sample_test

        self.is_bool = is_bool


def isPrime(x):
    if x < 2:
        return False

    for i in range(2, x):
        if x % i == 0:
            return False

    return True


def power(a, x):
    ans = 1

    for i in range(x):
        ans *= a

    return ans


function_data = {
    -1: Function_Data_Content(
        function_name="power",
        function_input="(x)",

        input_type=(int, int),
        input_range=((1, 200), (0, 100)),

        answer_function=power,
        sample_test=(0, 1, 2, 3, 5, 6, 7, 9),
    ),

    1: Function_Data_Content(
        function_name="isPrime",
        function_input="(x)",

        input_type=int,
        input_range=(11, 500),

        answer_function=isPrime,
        sample_test=(0, 1, 2, 3, 5, 6, 7, 9),

        is_bool=True
    )
}
