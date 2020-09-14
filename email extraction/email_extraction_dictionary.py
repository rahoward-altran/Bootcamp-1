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

    #print dictionary
    print("Dictionary")
    for domain, frequency in freq_dict.items():
        print(domain, frequency)

    print("----------------------------")
    print("sorted:")
    # dictionary is now a list of domains in decending frequency order
    freq_dict_sorted_list = [domain for domain, freq in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)]
    for i in range(10):
        print(freq_dict_sorted_list[i])


    #no check of input. dangerous to proceed
    print("----------------------------")
    userinput = input("Enter a number and domains with a higher frequency than it will be returned (unordered): ")
    for domain, freq in freq_dict.items():
        if freq >= int(userinput):
            print(domain, freq)

