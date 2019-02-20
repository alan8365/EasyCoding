from collections import Iterable
import random

from .codelib import *

random_test_counter = 30


def check_user_code(pk, code):
    is_answer_right = True

    final_output = []
    data = function_data[pk]

    local_var = {}

    exec(code, globals(), local_var)

    local_var['answer_function'] = data.answer_function

    if data.is_bool:
        random_number = {random.randint(0, random_test_counter - 1) for _ in range(15)}
        random_test_function = get_random_test_function(data.input_type, data.input_range)

        random_test = ()
        for i in range(random_test_counter):
            temp = random_function_to_random_test(random_test_function)
            if i in random_number:
                while data.answer_function(*temp):
                    temp = random_function_to_random_test(random_test_function)
            else:
                while not data.answer_function(*temp):
                    temp = random_function_to_random_test(random_test_function)
            random_test += temp

    else:
        random_test_function = get_random_test_function(data.input_type, data.input_range)
        if random_test_function == ():
            random_test = ()
        else:
            random_test = tuple((random_function_to_random_test(random_test_function) for _ in range(random_test_counter)))

    random_test = data.sample_test + random_test

    for i in random_test:
        # TODO fix display
        if isinstance(i, Iterable) and not isinstance(i, str):
            output = {"input": input_to_str(i)}
        else:
            output = {"input": i}

        user_result = execute_function(data.function_name, i, local_var)
        answer = execute_function('answer_function', i, local_var)

        if user_result == answer:
            output["is_answer_right"] = True
            output["output"] = str(user_result)
        else:
            is_answer_right = False
            output["is_answer_right"] = False
            output["answer"] = str(answer)
            output["output"] = str(user_result)

        final_output.append(output)

    return is_answer_right, final_output


def usercode_handler(signum, frame):
    raise TimeoutError("超過1分鐘")


def execute_function(function_name, input_var, local_var):
    if isinstance(input_var, str):

        exec_str = "user_result = %s('%s')" % (function_name, input_var)

    elif isinstance(input_var, Iterable):

        exec_str = "user_result = %s(*input_var)" % function_name

    else:
        exec_str = "user_result = %s(%s)" % (function_name, str(input_var))

    local_var["input_var"] = input_var
    exec(exec_str, globals(), local_var)

    return local_var['user_result']


def get_random_test(input_type, input_range, bool_answer_function=None):
    random_test = ()

    if isinstance(input_type, Iterable):

        all_random_test = ()

        for i, j in zip(input_type, input_range):
            all_random_test += (get_random_test(i, j),)

        return tuple(zip(*all_random_test))

    else:
        if input_type == int:
            def random_function() -> int:
                return random.randint(*input_range)
        elif input_type == float:
            def random_function() -> float:
                return round(random.uniform(*input_range), 2)
        elif input_type == str:
            def random_function() -> str:
                length = len(input_range) - 1
                return input_range[random.randint(0, length)]
        elif input_type == bool:
            def random_function() -> bool:
                return input_range[random.randint(0, 1)]
        elif input_type == tuple:
            def random_function() -> tuple:

                result = tuple()

                length_of_range = random.randint(*input_range.length_range)

                for _ in range(length_of_range):
                    result += (random.randint(*input_range.input_range),)

                return result
        elif input_type == list:
            def random_function() -> list:

                result = []

                length_of_range = random.randint(*input_range.length_range)

                for _ in range(length_of_range):
                    result += (random.randint(*input_range.input_range),)

                return result
        elif input_type == dict:
            pass


        else:
            return ()

    if bool_answer_function:
        random_number = {random.randint(0, random_test_counter - 1) for _ in range(15)}

        for i in range(random_test_counter):
            temp = random_function()

            if i in random_number:
                while not bool_answer_function(temp):
                    temp = random_function()

            random_test += (random_function(),)
    else:
        for _ in range(random_test_counter):
            random_test += (random_function(),)

    return random_test


def get_random_test_function(input_type: type, input_range):
    if isinstance(input_type, Iterable):

        all_random_test_function = tuple((get_random_test_function(i, j) for i, j in zip(input_type, input_range)))

        return all_random_test_function

    else:
        if input_type == int:
            def random_function() -> int:
                return random.randint(*input_range)
        elif input_type == float:
            def random_function() -> float:
                return round(random.uniform(*input_range), 2)
        elif input_type == str:
            def random_function() -> str:
                length = len(input_range) - 1
                return input_range[random.randint(0, length)]
        elif input_type == bool:
            def random_function() -> bool:
                return input_range[random.randint(0, 1)]
        elif input_type == tuple:
            def random_function() -> tuple:

                local_random_test_getter = get_random_test_function(input_range.input_type, input_range.input_range)

                length_of_range = random.randint(*input_range.length_range)

                result = tuple((local_random_test_getter() for _ in range(length_of_range)))

                return result
        elif input_type == list:
            def random_function():

                result = []

                length_of_range = random.randint(*input_range.length_range)

                for _ in range(length_of_range):
                    result += (random.randint(*input_range.input_range),)

                return result
        elif input_type == dict:
            pass

            def random_function():

                data = input_range.data

                data = {
                    key: get_random_test_function(*data[key])() for key in data.keys()
                }

                return data

        else:
            random_function = ()

    return random_function


def random_function_to_random_test(random_function):
    if isinstance(random_function, Iterable):

        print(tuple((random_function_to_random_test(i) for i in random_function)))
        return tuple((random_function_to_random_test(i) for i in random_function))

    else:

        return random_function()


def input_to_str(random_input) -> str:
    random_input = list(map(str, random_input))

    for i in range(len(random_input)):
        if '}' in random_input[i]:
            random_input[i] = random_input[i].replace('}', '}\n')

        if len(random_input[i]) > 15:
            random_input[i] = "\n" + random_input[i]

    return ' , '.join(random_input)
