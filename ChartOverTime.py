#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 03:38:47 2024

@author: chris
"""

import matplotlib.pyplot as plt

# Data pulled from the results of each month
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
total_transactions = [37781514, 34197339, 41500537, 38531321, 37764888, 33152534]
on_chain_transactions = [32245872, 29035639, 35199489, 31817882, 30913837, 26209286]
not_included_transactions = [5535642, 5161700, 6301048, 6713439, 6851051, 6943248]

# Create the chart
plt.figure(figsize=(12, 6))

# Calculate percentages for on-chain and not-included transactions
on_chain_percentages = [(on_chain / total) * 100 for on_chain, total in zip(on_chain_transactions, total_transactions)]
not_included_percentages = [(not_included / total) * 100 for not_included, total in zip(not_included_transactions, total_transactions)]


# Plot each transaction type
plt.plot(months, [x / 1e6 for x in total_transactions], label="Total Transactions", marker='o', linewidth=2)
plt.plot(months, [x / 1e6 for x in on_chain_transactions], label="On-Chain Transactions", marker='o', linewidth=2)
plt.plot(months, [x / 1e6 for x in not_included_transactions], label="Not Included Transactions", marker='o', linewidth=2)

# Customisation
plt.title("Transaction Trends (January - June 2024)", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Number of Transactions (in millions)", fontsize=12)
plt.legend(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate percentages on the on-chain and not-included transactions
for i, month in enumerate(months):
    plt.text(i, on_chain_transactions[i] / 1e6, f"{on_chain_percentages[i]:.1f}%", fontsize=10, ha='center', color='blue')
    plt.text(i, not_included_transactions[i] / 1e6, f"{not_included_percentages[i]:.1f}%", fontsize=10, ha='center', color='red')

# Customisation for the percentages
plt.title("Transaction Trends with Percentages (January - June 2024)", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Number of Transactions (in millions)", fontsize=12)
plt.legend(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the chart
plt.tight_layout()
plt.show()