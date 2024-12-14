#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 22:51:04 2024

@author: chris
"""

import pandas as pd
import os


file_directory = '/Volumes/NO NAME/FS/Mempool Dumpster/January'

# List all files in the directory for completness
print("Files in directory:")
print(os.listdir(file_directory))

# Initialize an empty list to stores the daily transactions
dataframes = []

# Counter to track total rows across all CSVs
total_rows_in_files = 0

# Loop through the daily files of Jan 2024
for day in range(1, 32):
    file_name = f"2024-01-{day:02d}.csv"  # Format day as 01, 02, etc.
    file_path = os.path.join(file_directory, file_name)
    
    if os.path.exists(file_path):
       
        df = pd.read_csv(file_path, delimiter=None, low_memory=False)
        file_row_count = df.shape[0]  # Count rows in the current file
        total_rows_in_files += file_row_count  # Add to the total row count
        print(f"{file_name}: {file_row_count} rows")  # Print the row count of the current file
        dataframes.append(df)
    else:
        print(f"File not found: {file_name}")


if dataframes:
    # Concatenate all data frames into one
    data_ori = pd.concat(dataframes, ignore_index=True)

    # Print the total rows in all files combined and the final concatenated data frame
    print(f"Total rows in all files: {total_rows_in_files}")
    print(f"Total rows in the concatenated DataFrame: {data_ori.shape[0]}")
else:
    print("No files were loaded. Please verify the file directory and file names.")

#-------------

#Ensure 'included_at_block_height' is numeric
data_ori['included_at_block_height'] = pd.to_numeric(data_ori['included_at_block_height'], errors='coerce')

# Calculate counts
on_chain_count = data_ori[data_ori['included_at_block_height'] > 0].shape[0]
not_included_count = data_ori[data_ori['included_at_block_height'].isna() | (data_ori['included_at_block_height'] == 0)].shape[0]

# Print results
print(f"On-chain transactions: {on_chain_count}")
print(f"Not included transactions: {not_included_count}")
