from typing import Dict, List, Type
import logging
import csv
import json
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from decimal import *
import re

# Attributes in this class is:
    # Date of transaction; the payer; payee; what the payment was for; and how much the payment was
# Methods in this class:
    # None
class Transaction:
    date: date
    fromAccount: str
    toAccount: str
    description: str
    amount: Decimal

    def __init__(self):
        self.date = datetime(2001, 1, 1, 0, 0)
        self.fromAccount = "From"
        self.toAccount = "To"
        self.description = "~~~"
        self.amount = Decimal(0)


# Attributes in this class is:
    # Account holder name; balance in account; and the list of transactions relevant to the account holder
# Methods in this class:
    # Add new transactions; update the balance
class Account:
    account_name: str
    balance: Decimal
    transactions: List[Transaction]

    def __init__(self):
        self.account_name = ""
        self.balance = Decimal(0)
        self.transactions = []

    def add_transaction(self, new_transaction):
        #new transaction is of type transaction. errors pre-handled
        self.transactions.append(new_transaction)


    def update_balance(self):
        self.balance = 0
        for transaction in self.transactions:
            # info : type(transaction) = Transaction
            tx = transaction.fromAccount
            rx = transaction.toAccount
            if self.account_name == tx:
                self.balance -= transaction.amount
            elif self.account_name == rx:
                self.balance += transaction.amount
            else:
                print("THIS SHOULD NEVER HAPPEN")
        logging.info("The balance has been updated for the account of  " + self.account_name)


# Attributes in this class is:
    # accounts which is a dictionary of {account holder name : account details}
# Methods in this class:
    # None
class SupportBank:
    accounts: Dict[str, Account]

    def __init__(self):
        self.accounts = {}


# FILE HANDLING FUNCTIONS-----------------------------------------------------------------------
# Add all the transactions from the files into the SupportBank
def read_transaction_file(bank):
    read_xml("Transactions2012.xml", bank)
    read_json("Transactions2013.json", bank)
    read_csv("Transactions2014.csv", bank)
    read_csv("DodgyTransactions2015.csv", bank)


# gets/creates bank accounts and executes 'Account.add_transaction(new_transaction)'
# code wasn't very DRY so added this function:
def get_account_add_transaction(bank, new_transaction):
    # info: setdefault() gets a value of the given key if it exists, else adds {key: defaultValue} to the dictionary
    # info: this is different to get() because get returns the value if key not found but does not modify the dictionary
    default_account_from: Type[Account] = Account()
    default_account_from.account_name = new_transaction.fromAccount
    default_account_to: Type[Account] = Account()
    default_account_to.account_name = new_transaction.toAccount

    # Update Payers account
    bank.accounts.setdefault(new_transaction.fromAccount, default_account_from).add_transaction(new_transaction)
    # Update Payee account
    bank.accounts.setdefault(new_transaction.toAccount, default_account_to).add_transaction(new_transaction)


# Verify that the date is in the expected format using reg expr
def format_date(date):
    if re.fullmatch("\d{2}/\d{2}/\d{4}", date) == None:
        logging.exception("Error: Data was the wrong format")
        raise ValueError("Date is in the wrong format")
    return date


# Convert ooxml date into day/month/year format
def ooxml_date_to_dmy(date):
    # ooxml date is the number of days since 1899-12-31
    # error with leap years - scr = comment online
    try:
        null_date = datetime(1899, 12, 31)
        new_date = null_date + timedelta(int(date))
        date_str = new_date.strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Date was in wrong format")
    return date_str


# read xml file and put all valid transaction into SupportBank
def read_xml(filename, bank):
    tree = ET.parse(filename)
    root = tree.getroot()
    # Does a recusive depth first iteration through the tree structure starting from root
    for transaction in root.findall('SupportTransaction'):
        new_transaction: Type[Transaction] = Transaction()
        try:
            new_transaction.date = ooxml_date_to_dmy(transaction.attrib['Date'])
            new_transaction.description = transaction.find('Description').text
            new_transaction.amount = Decimal(transaction.find('Value').text)
            parties = transaction.find('Parties')
            new_transaction.fromAccount = parties.find('From').text
            new_transaction.toAccount = parties.find('To').text
        except:
            print("Transaction in xml file was not as expected. It has been ignored")
            logging.exception("Transaction in file was not as expected. It has been ignored")
            continue

        # Get account of money sender and receiver and add new transaction
        get_account_add_transaction(bank, new_transaction)


# read json file and put all valid transaction into SupportBank
def read_json(filename, bank):
    with open(filename) as transactionFile:
        json_obj = json.load(transactionFile)
        for line in json_obj:
            new_transaction: Type[Transaction] = Transaction()
            try:
                dl = line['date'].split('-')
                date = dl[2] + "/" + dl[1] + "/" + dl[0]
                # info: if error not thrown yet format_date should be redundant
                new_transaction.date = format_date(date)
                new_transaction.fromAccount = line['fromAccount']
                new_transaction.toAccount = line['toAccount']
                new_transaction.description = line['narrative']
                # info: stored in file as float. need to convert to str first before convert to Decimal
                new_transaction.amount = Decimal(str(line['amount']))
            except:
                print("Transaction in json file was not as expected. It has been ignored")
                logging.exception("Transaction in file was not as expected. It has been ignored")
                exit(-1)
                # continue

            # Get account of money sender and receiver and add new transaction
            get_account_add_transaction(bank, new_transaction)


# read csv file and put all valid transaction into SupportBank
def read_csv(filename, bank):
    with open(filename) as transactionFile:
        csv_obj = csv.DictReader(transactionFile, delimiter=",")
        for line in csv_obj:
            new_transaction: Type[Transaction] = Transaction()
            try:
                new_transaction.date = format_date(line['Date'])
                new_transaction.fromAccount = line['From']
                new_transaction.toAccount = line['To']
                new_transaction.description = line['Narrative']
                new_transaction.amount = Decimal(line['Amount'])
            except:
                print("Transaction in csv file was not as expected. It has been ignored")
                logging.exception("Transaction in file was not as expected. It has been ignored")
                continue

            # Get account of money sender and receiver and add new transaction
            get_account_add_transaction(bank, new_transaction)


# handle request to import another file. Identify file type and execute corresponding function
def handle_file(filename, bank):
    if filename[-3:] == "csv":
        try:
            read_csv(filename, bank)
        except FileNotFoundError:
            print("File not found")
            logging.exception("File Not Found")
    elif filename[-4:] == "json":
        try:
            read_json(filename, bank)
        except FileNotFoundError:
            print("File not found")
            logging.exception("File Not Found")
    elif filename[-3:] == "xml":
        try:
            read_xml(filename, bank)
        except FileNotFoundError:
            print("File not found")
            logging.exception("File Not Found")
    else:
        print("File type not recognised")
        logging.exception("Couldn't process file type")
# END FILE HANDLING FUNCTIONS ---------------------------------------------------------------


# PRINT DATA FUNCTIONS -----------------------------------------------------------------------
# prints the names and balances of all accounts in SupportBank
def print_account_summary(bank):
    for account_name, account in bank.accounts.items():
        print(account_name, end=": ")
        print(account.balance)


# prints all transactions associated with an account name
def print_named_account(name, bank):
    if name in bank.accounts:
        print("Date | From | To | Naritive | Amount ")
        for transaction in bank.accounts.get(name).transactions:
            print(transaction.date, end=" | ")
            print(transaction.fromAccount, end=" | ")
            print(transaction.toAccount, end=" | ")
            print(transaction.description, end=" | ")
            print(transaction.amount)
    else:
        print("name not recognised. Name is case sensitive")
# END PRINT DATA FUNCTIONS -------------------------------------------------------------------


# MAIN ---------------------------------------------------------------------------------------
# Set up log
logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)
logging.info("Program has started and the log is open")

# Set up Bank
bank: Type[SupportBank] = SupportBank()
# Read Transactions from file into memory
read_transaction_file(bank)
logging.info("Success: transactions files have been read")

notExit = True
while notExit:

    user_input = input("Enter a command (list all or list [account name (case sensitive)] or import file [filename] or exit): ")
    logging.info("Success: user has entered " + user_input)
    user_input_caps = user_input.upper()

    if user_input_caps == "LIST ALL":
        # update balance
        for _, account in bank.accounts.items():
            account.update_balance()
        logging.info("Success: updated the balances for the accounts")
        # Print balances
        print_account_summary(bank)
        logging.info("Success: printed account summaries")

    elif user_input_caps[:4] == "LIST":
        name = user_input[5:]
        logging.info("looking for the transactions of " + name)
        print_named_account(name, bank)
        logging.info("Success: printed " + name + "'s transactions")

    elif user_input_caps[:11] == "IMPORT FILE":
        filename = user_input[12:]
        handle_file(filename, bank)

    elif user_input_caps == "EXIT":
        notExit = False
        logging.info("Successfully exiting program")

    else:
        print("Command not recognised")
        logging.warning("User input was not recognised")



