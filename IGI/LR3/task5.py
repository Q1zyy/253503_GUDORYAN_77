from utility import get_int_from_input
from utility import get_list_of_floats_from_keyboard
from utility import get_list_random
from utility import get_float_from_input

def print_list(lst:list):
    """Print list"""
    for item in lst:
        print(item)
        
def count_of_positive_numbers_greater(a:list[float], c:float) -> int:
    """Return count of numbers greater than c"""
    res = 0
    for val in a:
        res += (val > c and val > 0)
    return res

def get_index_of_max(a:list[float]) -> int:
    """Return index of max modulo element"""
    mx = abs(a[0])
    index = 0
    for i in range(1, len(a)):
        if abs(a[i]) > mx:
            mx = abs(a[i])
            index = i
    return index
        
def get_multiplication_after_max(a:list[float]) -> float:
    """Return multiplication of numbers after modulo max"""
    pos = get_index_of_max(a)
    if pos == len(a) - 1:
        return 0
    mul = a[pos + 1]
    for i in range(pos + 2, len(a)):
        mul *= a[i]
    return mul
    
def task5():
    """Return the number of positive elements of the list, large numbers C\n
    Returns the product of the list elements located after the max modulo element"""
    n = get_int_from_input('n')
    print('Input 1 to input from keyborad, 2 to random input')
    s = input()
    lst = []
    match s:
        case '1':
            lst = get_list_of_floats_from_keyboard(n)
        case '2':
            lst = get_list_random(n)
    
    c = get_float_from_input('c')
    print_list(lst)
    numbers_greater = count_of_positive_numbers_greater(lst, c)
    multiplication = get_multiplication_after_max(lst)
    return numbers_greater, multiplication
    