#   Gudoryan Evgeniy Svyatoslavovich
#   Laba 1
#   23503
#   v.1.0.0
#   28.03.2024

from task1 import task1
from task2 import task2
from task3 import task3
from task4 import task4
from task5 import task5

while True:
    print('Input 1-5 to chose task')
    s = input()
    match s:
        case "1":
            print(task1())
        case "2":
            print('Count of numbers less than 10 =', task2())
        case "3":
            lower_letters, diggits = task3()
            print(f'Number of lowercase letters = {lower_letters}\n'
                  f'Number of diggits = {diggits}')
        case "4":
            a, b, c = task4()
            print('Number of words starts from consonant =', a)
            print('Words with double letter and their indecies')
            for word, index in b:
                print(word, index)
            print('Words in alphabetic order');
            for word in c:
                print(word)
        case "5":
            numbers_greater, multiplication = task5()
            print('Numbers greater =', numbers_greater)
            print('Multiplication =', multiplication)
        case _:
            print('Incorrect option')
            