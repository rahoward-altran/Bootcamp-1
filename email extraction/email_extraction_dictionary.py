import re
from typing import Dict

filename = "sample.txt"
#freq_dict : Dict[domain :str, frequency: num]
freq_dict = {}

with open(filename) as file:
    data = file.read()
    #find all emails
    list = re.findall('\S+@\S+', data)

    for i in range(len(list)):
        domain = re.search("@\S+", list[i]).group(0)
        #Add to dictionary / increment entry
        freq_dict[domain] = freq_dict.get(domain, 0) + 1
    #ToDo: sort
    sorted(freq_dict)

    #print dictionary
    for domain, frequency in freq_dict.items():
        print(domain, frequency)
