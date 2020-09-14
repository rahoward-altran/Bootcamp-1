def fizzbuzz():
    for i in range(1,256):
        print_fizz = True
        a = ""

        if i%3 == 0 and i%13 == 0:
            #ToDo: unclear in instructions for case %17
            #check17(i, a, "FizzFezz")
            a = a + "FizzFezz"
            print_fizz = False
        elif i%13 == 0:
            a = check17(i, a, "Fezz")

        if i%11 == 0:
            a = check17(i, a, "Bong")
        if i%3 == 0 and print_fizz:
            a = check17(i ,a, "Fizz")
        if i%5 == 0:
            a = check17(i, a, "Buzz")
        if i%7 == 0:
            a = check17(i, a,"Bang")

        #print number if nothing else has been set
        if a == "":
            a = str(i)
        #print line
        print(a)

def check17(i, old_string,newstring):
    if i%17 == 0:
        return newstring + old_string
    else:
        return old_string + newstring

fizzbuzz()