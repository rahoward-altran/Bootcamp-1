filename = "sample.txt"

with open(filename) as file:
    data = file.read()
    counter = 0
    for i in range(0, len(data)):
        if data[i: i+14] == "@softwire.com " or data[i: i+14]== "@softwire.com\n":
            counter += 1
    print(counter)

