import re
filename = "sample.txt"

with open(filename) as file:
    data = file.read()
    list = re.findall('\S+@softwire.com\s', data)
    print(len(list))

