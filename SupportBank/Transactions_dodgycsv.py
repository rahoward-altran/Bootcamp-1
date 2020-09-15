import csv
from decimal import *
import logging


def readtransactionfile():
    filename = "DodgyTransactions2015.csv"
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
        date = line[0]
        tx = line[1]
        rx = line[2]
        description = line[3]
        try:
            amount = Decimal(line[4])*100
            account_summary_dict[tx] = account_summary_dict.get(tx, 0) - amount
            account_summary_dict[rx] = account_summary_dict.get(rx, 0) + amount
        except InvalidOperation:
            message = "The amount for entry " + \
                        "Date: " + date + \
                        ", From: " + tx + \
                        ", To: " + rx + \
                        ", Narrative: " + description + \
                        " is INVALID"
            logging.exception(message)

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


logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)
logging.info("Program has started and the log is open")
data = readtransactionfile()
logging.info("Success: transaction file has been read")
account_summary_dict = create_account_summary(data)
logging.info("Success: dictionary of account summaries has been created")

userinput = input("Enter a command (list all or list [account name]): ")
logging.info("Success: user has entered " + userinput)
userinput = userinput.upper()

if userinput == "LIST ALL":
    logging.info("listing all account summaries")
    for name, value in account_summary_dict.items():
        print(name, end="")
        if value < 0:
            print(" owes £", abs(value)/100)
        elif value > 0:
            print(" is owed £", abs(value)/100)
        else:
            print("'s account is settled")
    logging.info("Success: printed summaries")
elif userinput[:4] == "LIST":
    name = userinput[5:]
    logging.info("looking for the tranactions of " + name)
    print_named_account(name, data)
    logging.info("Success: printed " + name + "'s transactions")
else:
    logging.warning("User input was not recognised")

