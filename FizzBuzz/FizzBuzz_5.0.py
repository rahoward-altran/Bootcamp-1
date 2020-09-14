def parse_input(ruleinput):
    flag_list = [False, False, False, False, False, False]
    for i in range(0,len(ruleinput)):
        x = int(ruleinput[i])
        if x == 3:
            flag_list[0] = True
        elif x == 5:
            flag_list[1] = True
        elif x == 7:
            flag_list[2] = True
        elif x == 11:
            flag_list[3] = True
        elif x == 13:
            flag_list[4] = True
        elif x == 17:
            flag_list[5] = True
        else:
            print("invalid rule entered")
    return flag_list

def converttostr(input_seq, seperator):
   # Join all the strings in list
   final_str = seperator.join(input_seq)
   return final_str

def fizzbuzz(flag_list, range_top):
    for i in range(1, range_top + 1):
        a = []
        string = ""

        if flag_list[0] and i%3 == 0:
            a.append("Fizz")
        if flag_list[4] and i%13 ==0:
            a.append("Fezz")
        if flag_list[1] and i%5 == 0:
            a.append("Buzz")
        if flag_list[2] and i%7 == 0:
            a.append("Bang")
        if flag_list[3] and i%11 == 0:
            a.clear()
            if flag_list[4] and i % 13 == 0:
                a.append("Fezz")
            a.append("Bong")

        # print number if nothing else has been set
        if a == []:
            string = str(i)
        else:
            if flag_list[5] and i%17 == 0:
                a.reverse()
            string = converttostr(a, '')
        # print line
        print(string)

print("You can apply the following rules:")
print("multiples of 3: 'Fizz'")
print("multiples of 5: 'Buzz'")
print("multiples of 7: 'Bang'")
print("multiples of 11: 'Bong'")
print("multiples of 13: 'Fezz'")
print("multiples of 17: reverse")
count = input("How many rules would you like to apply?: ")
rule_list = []
print("Enter the rules you would like to apply one at a time")
for i in range(0, int(count)):
    rule_list.append(int(input()))
print("you have have selected: ", end="")
print(rule_list)
flag_list = parse_input(rule_list)
print(flag_list)
range_top = input("Enter the maximum number: ")
#no validation on user input dangerous to proceed
fizzbuzz(flag_list, int(range_top))

