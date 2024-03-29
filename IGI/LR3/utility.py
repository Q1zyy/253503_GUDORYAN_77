from random import uniform

def decorator(func):
    """Decorator to see which function works"""
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__}\n{func.__doc__}")
        return func(*args, **kwargs)
    return wrapper

def is_float(x) -> bool:
    """Check if number is float"""
    try:
        float(x)
        return True
    except:
        print('Not a float number')
        return False

def is_int(x) -> bool:
    """Check if number is integer"""
    try:
        int(x)
        return True
    except:
        print('Not a integer number')
        return False

@decorator
def get_float_from_input(name:str) -> float:
    """Get float number float input"""
    print('Input', name)
    x = input()
    while not is_float(x):
        print(f'Input {name} again')
        x = input()
    return float(x)

def get_int_from_input(name:str) -> int:
    """Get float number int input"""
    print('Input', name)
    x = input()
    while not is_int(x):
        print(f'Input {name} again')
        x = input()
    return int(x)

def get_list_of_floats_from_keyboard(n:int) -> list[float]:
    """Return list entering from keyboard"""
    res = []
    for i in range(n):
        res.append(get_float_from_input('number'))
    return res

def random_generator(n:int):
    """Return random float number from -50 to 50"""
    for i in range(n):
        yield uniform(-50, 50)

def get_list_random(n:int) -> list[float]:
    """Return list with random items with lenght n"""
    res = []
    gen = random_generator(n)
    for i in range(n):
        res.append(next(gen))
    return res
