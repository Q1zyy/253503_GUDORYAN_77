def task3():
    """In the line entered from the keyboard, returns the number of lowercase letters and numbers"""
    print('Input string')
    s = input()
    diggits = 0
    lower_letters = 0
    for c in s:
        if c.isdigit():
            diggits += 1
        if c.islower():
            lower_letters += 1
    return lower_letters, diggits