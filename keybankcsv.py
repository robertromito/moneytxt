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

def write_means(title, means):
    print("{0:50}\033[1;{2}m{1:10,.2f}\033[1;m"
          .format(title, means, "41" if means < 0 else ""))

if len(sys.argv) < 2:
   print(f'usage: keybankcsv.py [glob path of keybank csv files dir]')
   exit(1)

print("Analysys of Key Bank csv download files:")

total_means = 0
for csv in sys.argv[1:]:
    with open(csv, 'r') as f:
        transactions = f.readlines()
        accounts = split_by_account(transactions)
        print(f'\n\033[1;44m{csv:60}\033[1;m\n')
        for account in accounts:
            write_means(account[0].rstrip(), sum_transactions_for(account))
        csv_means = sum_transactions_for(transactions)
        write_means("Total", csv_means)
        total_means += csv_means

print("\n")
write_means("Grand Total", total_means)
