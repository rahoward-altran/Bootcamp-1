import csv

def readtransactionfile():
    filename = "Transactions2014.csv"
    data = []
    with open(filename) as transactionFile:
        csv_obj = csv.reader(transactionFile, delimiter=",")
        for line in csv_obj:
            data.append(line)
    return data

def create_account_summary(data):
    account_summary_dict = {}
    first_line = True
    for line in data:
        if first_line:
            #ignore header
            first_line = False
            continue
        #date = line[0]
        tx = line[1]
        rx = line[2]
        # description = line[3]
        amount = int(float(line[4])*100)
        account_summary_dict[tx] = account_summary_dict.get(tx, 0) - amount
        account_summary_dict[rx] = account_summary_dict.get(rx, 0) + amount
    return account_summary_dict



def print_named_account(name, data):
    first_line = True
    for line in data:
        if first_line:
            print(line)
            first_line = False
            continue
        date = line[0]
        tx = line[1]
        rx = line[2]
        description = line[3]
        amount = line[4]
        if tx.upper() == name:
            amount = "-" + amount
            print(date, tx, rx, description, amount)
        elif rx.upper() == name:
            print(date, tx, rx, description, amount)


data = readtransactionfile()
print(data)
account_summary_dict = create_account_summary(data)

userinput = input("Enter a command (list all or list [account name]: ")
userinput = userinput.upper()

if userinput == "LIST ALL":
    for name, value in account_summary_dict.items():
        print(name, end="")
        if value < 0:
            print(" owes £", abs(value)/100)
        elif value > 0:
            print(" is owed £", abs(value)/100)
        else:
            print("'s account is settled")
elif userinput[:4] == "LIST":
    name = userinput[5:]
    print_named_account(name, data)

