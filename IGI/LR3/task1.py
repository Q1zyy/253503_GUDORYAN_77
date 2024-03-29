import math
from utility import get_float_from_input

def power_series_generator(x):
    """Generates the next sum of decomposition"""
    res = 0
    n = 0
    while True:
        res += math.pow(-1, n) * math.pow(x, 2*n) / math.factorial(2*n)
        n += 1
        yield res

def task1():
    """Decompositions of a function into a power series and returns table"""
    x = get_float_from_input('x')
    eps = get_float_from_input('eps')
    s = str()
    n = 0
    result = math.cos(x)
    my_result = 0
    gen = power_series_generator(x)
    while n <= 500 and math.fabs(result - my_result) > eps:
        my_result = next(gen)
        s += f'{x}\t\t{n}\t\t{format(my_result, ".6f")}\t\t{format(result, ".6f")}\t\t{format(abs(my_result - result), ".6f")}\n'
        n += 1
    return s