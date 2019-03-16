#!/usr/bin/env python3
import sys


def split_by_account(csv):
    accounts = []
    current_account = None
    for line in csv:
        if line == "\n":
            if current_account is not None:
                accounts.append(current_account)
            current_account = []
        else:
            current_account.append(line)

    if current_account:
        accounts.append(current_account)

    return accounts

def amount_to_money(amount_string):
    try:
        return float(amount_string.replace('"',''))
    except ValueError:
        return 0.0

def sum_transactions_for(keybank_csv):
    transaction_amounts = [amount_to_money((f.split(",")[1]))
                           for f in keybank_csv
                           if '"' in f]
    return sum(transaction_amounts)

print("Welcome to the KeyBank bank account csv analyzer")

if len(sys.argv) < 2:
   print(f'usage: keybankcsv.py [glob path of keybank csv files dir]')
   exit(1)

total_means = 0
for csv in sys.argv[1:]:
    with open(csv, 'r') as f:
        transactions = f.readlines()
        accounts = split_by_account(transactions)
        print(f'\n{csv}')
        for account in accounts:
            account_means = sum_transactions_for(account)
            print(f'{account[0].rstrip()}: {account_means:10,.2f}')
        csv_means = sum_transactions_for(transactions)
        print(f'Total: {csv_means:10,.2f}')
        total_means += csv_means

print(f'\nGrand Total: {total_means:10,.2f}')
