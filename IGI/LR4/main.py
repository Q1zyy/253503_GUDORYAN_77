import utility
import task1
import task2
import task3
import task4
import task5

while True:
    print("1 - Students")
    print("2 - Text analyzis")
    print("3 - Cos approximation ")
    print("4 - Hexagon")
    print("5 - Matrix operations")
    print("6 - exit")
    t = utility.get_int_from_input('option')
    if t == 1:
        task1.main()
    if t == 2:
        task2.main()
    if t == 3:
        task3.main()
    if t == 4:
        task4.main()
    if t == 5:
        task5.main()
    if t == 6:
        break
    