def split_string_function(s):
    digits = ""
    operators = "+-*/x"

    for char in s:
        if char in operators:
            return [digits, char]
        else:
            digits += char

    return [digits]


def split_strings(input_string):
    result = split_string_function(input_string)
    operator = result.pop()
    result = str(result[0])

    return result, operator
