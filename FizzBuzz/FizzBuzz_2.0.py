def fizzbuzz():
    for i in range(1,101):
        num = True
        print_fizz = True

        if i%3 == 0 and i%13 == 0:
            print("FizzFezz" , end = "")
            print_fizz = False
            num = False
        elif i%13 == 0:
            print("Fezz", end ="")
            num = False
        if i%11 == 0:
            print("Bong")
            continue
        if i%3 == 0 and print_fizz:
            print("Fizz", end ="")
            num = False
        if i%5 == 0:
            print("Buzz", end ="")
            num = False
        if i%7 == 0:
            print("Bang", end ="")
            num = False
        if num:
            print(i, end="")
        print()



fizzbuzz()