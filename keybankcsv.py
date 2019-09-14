#!/usr/bin/env python3
import sys
import os
import json

screen_rows, screen_cols = os.popen('stty size', 'r').read().split()
title_width = 40 
amount_width = 10 

def get_config(args):
    config = {}
    config_file = os.getcwd() + "/moneytxt.json"
    if os.path.isfile(config_file):
        print(f'Reading config')
        with open(config_file, 'r') as f:
            config = json.loads(f.read())
    config["accounts_to_analyze"] = ([arg.replace('--', '') for arg in args if arg.startswith('--')] + ['all'])[0]            
    return config

def should_analyze(account_id, config):
    if config["accounts_to_analyze"] == 'all': return True
    if config["accounts_to_analyze"] not in config: return True
    if account_id.startswith(tuple(config[config["accounts_to_analyze"]])): return True
    return False


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

def transaction_amount(transaction):
    return transaction.split(",")[1]

def amount_to_money(amount_string):
    try:
        return float(amount_string.replace('"',''))
    except ValueError:
        return 0.0

def sum_transactions_for(keybank_csv):
    return sum([amount_to_money((transaction_amount(f)))
                for f in keybank_csv
                if '"' in f])

def write_means(title, means, transaction_highlight = ""):
    return "{0:{3}}\033[1;{2}m{1:{4},.2f}\033[1;m\t{5:50}".format(
            title, 
            means, 
            "41" if means < 0 else "", 
            title_width,
            amount_width,
            transaction_highlight)

def transaction_sort_key(t):
    return amount_to_money(transaction_amount(t))

def most_expensive_transaction(account):
    if len(account) == 2:
        return ""
    else:
        sorted_transactions = sorted(account, key=transaction_amount, reverse=True)
        transaction_count = len(sorted_transactions)
        #return sorted_transactions[transaction_count - 3]
        return sorted_transactions[2]

##########

if len(sys.argv) < 2:
   print(f'usage: {sys.argv[0]} [glob path of keybank csv files dir]')
   exit(1)

config = get_config(sys.argv[1:])

print("Analysys of Key Bank csv download files:")
results = []

total_means = 0
for csv in [arg for arg in sys.argv[1:] if not arg.startswith('--')]:
    with open(csv, 'r') as f:
        csv_means = 0
        transactions = f.readlines()
        accounts = split_by_account(transactions)
        results.append(f'\n\033[1;44m{csv:{screen_cols}}\033[1;m\n')
        for account in accounts:
            account_id = account[0].rstrip()
            if should_analyze(account_id, config):
                account_means = sum_transactions_for(account)
                transaction_highlight = most_expensive_transaction(account) 
                csv_means += account_means
                results.append(write_means(account_id,account_means, transaction_highlight))
        results.append(write_means("Total", csv_means))
        total_means += csv_means
        results.append("")
        results.append(write_means("Grand Total", total_means))

[print(r) for r in results]
