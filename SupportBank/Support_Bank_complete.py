import csv
import json
from decimal import *
import logging
import xml.etree.ElementTree as ET
from _datetime import datetime, timedelta


def ooxml_date_to_dmy(date):
    # ooxml date is the number of days since 1899-12-31
    # error with leap years
    null_date = datetime(1899, 12, 31)
    new_date = null_date + timedelta(int(date))
    date_str = new_date.strftime("%d/%m/%Y")
    return date_str


def handle_file(filename, data):
    if filename[-3:] == "csv":
        try:
            read_csv(filename, data)
        except FileNotFoundError:
            print("File not found")
            logging.exception("File Not Found")
    elif filename[-4:] == "json":
        try:
            read_json(filename, data)
        except FileNotFoundError:
            print("File not found")
            logging.exception("File Not Found")
    elif filename[-3:] == "xml":
        try:
            read_xml(filename, data)
        except FileNotFoundError:
            print("File not found")
            logging.exception("File Not Found")
    else:
        print("File type not recognised")
        logging.exception("Couldn't process file type")
    return data


def read_transaction_file(empty_data):
    data_temp = read_xml("Transactions2012.xml", empty_data)
    data_temp = read_json("Transactions2013.json", data_temp)
    data_temp = read_csv("Transactions2014.csv", data_temp)
    full_data = read_csv("DodgyTransactions2015.csv", data_temp)
    return full_data



def read_xml(filename, data):
    tree = ET.parse(filename)
    root = tree.getroot()
    # Does a recusive depth first iteration through the tree structure starting from root
    for transaction in root.findall('SupportTransaction'):
        date = transaction.attrib['Date']
        description = transaction.find('Description').text
        amount = transaction.find('Value').text
        parties = transaction.find('Parties')
        tx = parties.find('From').text
        rx = parties.find('To').text
        date = ooxml_date_to_dmy(date)
        #
        data.append({'Date': date, 'From': tx, 'To': rx, 'Narrative': description, 'Amount': amount})
    return data


def read_json(filename, data):
    with open(filename) as transactionFile:
        json_obj = json.load(transactionFile)
        # json_obj is a python dict
        for line in json_obj:
            tx = line['fromAccount']
            rx = line['toAccount']
            description = line['narrative']
            amount = str(line['amount'])
            dl = line['date'].split('-')
            date = dl[2] + "/" + dl[1] + "/" + dl[0]
            #
            data.append({'Date': date, 'From': tx, 'To': rx, 'Narrative': description, 'Amount': amount})
    return data


def read_csv(filename, data):
    with open(filename) as transactionFile:
        csv_obj = csv.DictReader(transactionFile, delimiter=",")
        for line in csv_obj:
            #
            data.append(line)
    return data


def create_account_summary(data):
    account_summary = {}
    for line in data:
        tx = line['From']
        rx = line['To']
        try:
            amount = Decimal(line['Amount'])*100
            account_summary[tx] = account_summary.get(tx, 0) - amount
            account_summary[rx] = account_summary.get(rx, 0) + amount
        except InvalidOperation:
            date = line['Date']
            description = line['Narrative']
            message = "The amount for entry " + \
                      "Date: " + date + \
                      ", From: " + tx + \
                      ", To: " + rx + \
                      ", Narrative: " + description + \
                      " is INVALID"
            logging.exception(message)
    return account_summary


def print_account_summary_dict(account_summary_dict):
    for name, value in account_summary_dict.items():
        print(name, end="")
        if value < 0:
            print(" owes £", abs(value) / 100)
        elif value > 0:
            print(" is owed £", abs(value) / 100)
        else:
            print("'s account is settled")


def print_named_account(name, data):
    for k in data[0].keys():
        print(k, end=" ")
    print("")
    for line in data:
        date = line['Date']
        tx = line['From']
        rx = line['To']
        description = line['Narrative']
        amount = line['Amount']

        if tx.upper() == name:
            amount = "-" + amount
            print(date, tx, rx, description, amount)
        elif rx.upper() == name:
            print(date, tx, rx, description, amount)
        else:
            continue


# PROGRAM START
# set up log
logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)
logging.info("Program has started and the log is open")

# Read Transactions from file into memory
empty_data = []
data = read_transaction_file(empty_data)
logging.info("Success: transactions files have been read")


notExit = True
while notExit:

    user_input = input("Enter a command (list all or list [account name] or import file [filename] or exit): ")
    logging.info("Success: user has entered " + user_input)
    user_input_caps = user_input.upper()

    if user_input_caps == "LIST ALL":
        account_summary_dict = create_account_summary(data)
        logging.info("Success: dictionary of account summaries has been created")
        print_account_summary_dict(account_summary_dict)
        logging.info("Success: printed account summaries")

    elif user_input_caps[:4] == "LIST":
        name = user_input_caps[5:]
        logging.info("looking for the transactions of " + name)
        print_named_account(name, data)
        logging.info("Success: printed " + name + "'s transactions")

    elif user_input_caps[:11] == "IMPORT FILE":
        filename = user_input[12:]
        data = handle_file(filename, data)
    elif user_input_caps == "EXIT":
        notExit = False
        logging.info("Successfully exiting program")
    else:
        print("Command not recognised")
        logging.warning("User input was not recognised")

