filename = "sample.txt"

with open(filename) as file:
    data = file.read()
    counter = 0
    for i in range(0, len(data)):
        if data[i: i+13] == "@softwire.com":
            print("found")
            counter += 1
    print(counter)

