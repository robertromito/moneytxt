#!/usr/bin/env python3
import sys
import os

screen_rows, screen_cols = os.popen('stty size', 'r').read().split()
title_width = 40 
amount_width = 10 

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
    return sum([amount_to_money((f.split(",")[1]))
                for f in keybank_csv
                if '"' in f])

def write_means(title, means):
    return "{0:{3}}\033[1;{2}m{1:{4},.2f}\033[1;m".format(
            title, 
            means, 
            "41" if means < 0 else "", 
            title_width,
            amount_width)

if len(sys.argv) < 2:
   print(f'usage: keybankcsv.py [glob path of keybank csv files dir]')
   exit(1)

print("Analysys of Key Bank csv download files:")

results = []

total_means = 0
for csv in sys.argv[1:]:
    with open(csv, 'r') as f:
        transactions = f.readlines()
        accounts = split_by_account(transactions)
        results.append(f'\n\033[1;44m{csv:{screen_cols}}\033[1;m\n')
        for account in accounts:
            account_means = sum_transactions_for(account)
            results.append(write_means(account[0].rstrip(),account_means))
        csv_means = sum_transactions_for(transactions)
        results.append(write_means("Total", csv_means))
        total_means += csv_means
        results.append("")
        results.append(write_means("Grand Total", total_means))

[print(r) for r in results]
