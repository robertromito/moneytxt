#!/usr/bin/env python3
import sys

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
        csv_means = sum_transactions_for(f.readlines())
        print(f'{csv}: {csv_means:10,.2f}')
        total_means += csv_means

print(f'Total: {total_means:10,.2f}')
