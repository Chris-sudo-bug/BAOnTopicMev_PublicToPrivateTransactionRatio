#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:49:36 2024

@author: chris
"""

import pandas as pd
import os
import matplotlib.pyplot as plt


file_directory = '/Volumes/NO NAME/FS/Mempool Dumpster/February'

# List all files in the directory for completness
print("Files in directory:")
print(os.listdir(file_directory))

# Initialize an empty list to store dataframes
dataframes = []

# Counter to track total rows across all CSVs
total_rows_in_files = 0

# Lists for daily counts
daily_on_chain = []
daily_not_included = []
days = []

# Loop through the daily files of Feb 2024
for day in range(1, 30):  
    file_name = f"2024-02-{day:02d}.csv"  # Format day as 01, 02, etc.
    file_path = os.path.join(file_directory, file_name)
    
    if os.path.exists(file_path):
        
        df = pd.read_csv(file_path, delimiter=None, low_memory=False)
        file_row_count = df.shape[0]  # Count rows in the current file
        total_rows_in_files += file_row_count  # Add to the total row count
        print(f"{file_name}: {file_row_count} rows")  # Print the row count of the current file
        
        # Ensure 'included_at_block_height' is numeric
        df['included_at_block_height'] = pd.to_numeric(df['included_at_block_height'], errors='coerce')

        # Calculate daily counts
        on_chain_count = df[df['included_at_block_height'] > 0].shape[0]
        not_included_count = df[df['included_at_block_height'].isna() | (df['included_at_block_height'] == 0)].shape[0]

        # Append daily counts and day
        daily_on_chain.append(on_chain_count)
        daily_not_included.append(not_included_count)
        days.append(day)

        # Append the DataFrame to the list
        dataframes.append(df)
    else:
        print(f"File not found: {file_name}")


if dataframes:
    # Concatenate all data frames into one
    data_ori = pd.concat(dataframes, ignore_index=True)
    

    print(f"Total rows in all files: {total_rows_in_files}")
    print(f"Total rows in the concatenated DataFrame: {data_ori.shape[0]}")
    
    # Calculate overall counts
    on_chain_count = data_ori[data_ori['included_at_block_height'] > 0].shape[0]
    not_included_count = data_ori[data_ori['included_at_block_height'].isna() | (data_ori['included_at_block_height'] == 0)].shape[0]

    # Print results
    print(f"On-chain transactions: {on_chain_count}")
    print(f"Not included transactions: {not_included_count}")

    #-------Plot below
   
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
    plt.title("Daily Distribution of Transactions (February 2024)", fontsize=14)
    plt.ylabel("Number of Transactions", fontsize=12)
    plt.xlabel("Transaction Type", fontsize=12)
    plt.ylim(0, max(daily_data["On-Chain Transactions"].max(), daily_data["Not Included Transactions"].max()) * 1.2)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()
else:
    print("No files were loaded. Please verify the file directory and file names.")
