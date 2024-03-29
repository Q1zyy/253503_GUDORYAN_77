from utility import get_int_from_input

def task2():
    """Input integers from the keyboard and counts the count of numbers less than the number 10"""
    res = 0
    while True:
        x = get_int_from_input('number')
        res += (x < 10)
        if x == 100:
            return res