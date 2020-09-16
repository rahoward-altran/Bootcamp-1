import csv
import json
from decimal import *
import logging
import xml.etree.ElementTree as ET
from _datetime import datetime, timedelta


def ooxmlDateToYMD(date):
    # ooxml date is the number of days since 1899-12-31
    # error with leap years
    nullDate = datetime(1899, 12, 31)
    newdate = nullDate + timedelta(int(date))
    date_str = newdate.strftime("%d/%m/%Y")
    return date_str

def handlefile(filename, data):
    if filename[-3:] == "csv":
        try:
            readcsv(filename, data)
        except FileNotFoundError:
            print("File not found")
            logging.exception("File Not Found")
    elif filename[-4:] == "json":
        try:
            readJson(filename, data)
        except FileNotFoundError:
            print("File not found")
            logging.exception("File Not Found")
    elif filename[-3:] == "xml":
        try:
            readXML(filename, data)
        except FileNotFoundError:
            print("File not found")
            logging.exception("File Not Found")
    else:
        print("File type not recognised")
        logging.exception("Couldn't process file type")
    return data

def readtransactionfile(data):
    data = readXML("Transactions2012.xml", data)
    data = readJson("Transactions2013.json", data)
    data = readcsv("Transactions2014.csv", data)
    data = readcsv("DodgyTransactions2015.csv", data)
    return data

def readXML(filename, data):
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
        #ToDO convert date
        date = ooxmlDateToYMD(date)
        data.append([date, tx, rx, description, amount])
    return data




def readJson(filename, data):
    with open(filename) as transactionFile:
        json_obj = json.load(transactionFile)
        #json_obj is a python dict
        for line in json_obj:
            tx = line['fromAccount']
            rx = line['toAccount']
            description = line['narrative']
            amount = str(line['amount'])
            try:
                dl = line['date'].split('-')
                date = dl[2] + "/" + dl[1] + "/" + dl[0]
            except:
                message = "The Date for entry " + \
                          ", From: " + tx + \
                          ", To: " + rx + \
                          ", Narrative: " + description + \
                          ", Amount:" + amount + \
                          " is INVALID"
                logging.exception(message)

            data.append([date, tx, rx, description, amount])
    return data

def readcsv(filename, data):
    with open(filename) as transactionFile:
        first_line = True
        csv_obj = csv.reader(transactionFile, delimiter=",")
        for line in csv_obj:
            if first_line:
                # ignore header
                first_line = False
                continue
            #print(line)
            data.append(line)
    return data

def create_account_summary(data):
    account_summary_dict = {}
    for line in data:
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
    for line in data:
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

#set up log
logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)
logging.info("Program has started and the log is open")

data = []
data = readtransactionfile(data)
logging.info("Success: transaction file has been read")


notExit = True
while(notExit):

    userinput = input("Enter a command (list all or list [account name] or import file [filename] or exit): ")
    logging.info("Success: user has entered " + userinput)
    userinputcaps = userinput.upper()

    if userinputcaps == "LIST ALL":
        account_summary_dict = create_account_summary(data)
        logging.info("Success: dictionary of account summaries has been created")

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

    elif userinputcaps[:4] == "LIST":
        name = userinputcaps[5:]
        logging.info("looking for the transactions of " + name)
        print_named_account(name, data)
        logging.info("Success: printed " + name + "'s transactions")
    elif userinputcaps[:11] == "IMPORT FILE":
        filename = userinput[12:]
        data = handlefile(filename, data)
    elif userinputcaps == "EXIT":
        notExit = False
        logging.info("successfullly exiting program")
    else:
        print("Command not recognised")
        logging.warning("User input was not recognised")

