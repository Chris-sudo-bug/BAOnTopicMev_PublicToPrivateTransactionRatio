#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:35:39 2024

@author: chris
"""
import os
import pandas as pd
import matplotlib.pyplot as plt



file_directory = '/Volumes/NO NAME/FS/Mempool Dumpster/January'

# List all files in the directory for completeness
print("Files in directory:")
print(os.listdir(file_directory))

# Lists for daily counts
daily_on_chain = []
daily_not_included = []
days = []

# Loop through the daily files of Jan 2024
for day in range(1, 32):
    file_name = f"2024-01-{day:02d}.csv"  # Format day as 01, 02, etc.
    file_path = os.path.join(file_directory, file_name)
    
    if os.path.exists(file_path):
        
        df = pd.read_csv(file_path, delimiter=None, low_memory=False)
        df['included_at_block_height'] = pd.to_numeric(df['included_at_block_height'], errors='coerce')

        # Calculate daily counts
        on_chain_count = df[df['included_at_block_height'] > 0].shape[0]
        not_included_count = df[df['included_at_block_height'].isna() | (df['included_at_block_height'] == 0)].shape[0]

        # Append to lists
        daily_on_chain.append(on_chain_count)
        daily_not_included.append(not_included_count)
        days.append(day)

# Create a data frame for visualisation
daily_data = pd.DataFrame({
    "Day": days,
    "On-Chain Transactions": daily_on_chain,
    "Not Included Transactions": daily_not_included
})

 # Customisation 1 (larger box)
plt.figure(figsize=(12, 6))
plt.boxplot(
    [daily_data["On-Chain Transactions"], daily_data["Not Included Transactions"]],
    labels=["On-Chain Transactions", "Not Included Transactions"],
    widths=0.4  # Increase the box width
)

 # Customisation 2
plt.title("Daily Distribution of Transactions (January 2024)", fontsize=14)
plt.ylabel("Number of Transactions", fontsize=12)
plt.xlabel("Transaction Type", fontsize=12)
plt.ylim(0, max(daily_data["On-Chain Transactions"].max(), daily_data["Not Included Transactions"].max()) * 1.2)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()

