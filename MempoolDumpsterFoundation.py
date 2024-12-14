#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 21:55:10 2024

@author: chris
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



os.chdir('/Volumes/NO NAME/FS/Mempool Dumpster')
data_ori = pd.read_csv('2024-01-01.csv', delimiter=None, low_memory=False)

#Imp. for the first 20 columns
print(data_ori.head(20))
total_rows = data_ori.shape[0]
print(total_rows)
print(data_ori.columns)


# Ensure 'included_at_block_height' is numeric
data_ori['included_at_block_height'] = pd.to_numeric(data_ori['included_at_block_height'], errors='coerce')

# Calculate counts
on_chain_count = data_ori[data_ori['included_at_block_height'] > 0].shape[0]
not_included_count = data_ori[data_ori['included_at_block_height'].isna() | (data_ori['included_at_block_height'] == 0)].shape[0]

# Print results
print(f"On-chain transactions: {on_chain_count}")
print(f"Not included transactions: {not_included_count}")

#-----------

# Define a function to calculate statistics for each source
def calculate_stats(group):
    total = len(group)
    included = group[group['included_at_block_height'] > 0].shape[0]
    not_included = total - included
    included_pct = (included / total) * 100 if total > 0 else 0
    not_included_pct = (not_included / total) * 100 if total > 0 else 0
    return pd.Series({
        'TRANSACTIONS': total,
        'INCLUDED_ON_CHAIN': included,
        'INCLUDED_PCT': included_pct,
        'NOT_INCLUDED': not_included,
        'NOT_INCLUDED_PCT': not_included_pct
    })

# Group by 'sources' and calculate statistics
stats = data_ori.groupby('sources').apply(calculate_stats)

# Format the table for better readability
stats['TRANSACTIONS'] = stats['TRANSACTIONS'].apply(lambda x: f"{x:,}")
stats['INCLUDED_ON_CHAIN'] = stats['INCLUDED_ON_CHAIN'].apply(lambda x: f"{x:,}")
stats['NOT_INCLUDED'] = stats['NOT_INCLUDED'].apply(lambda x: f"{x:,}")
stats['INCLUDED_PCT'] = stats['INCLUDED_PCT'].apply(lambda x: f"{x:.1f}%")
stats['NOT_INCLUDED_PCT'] = stats['NOT_INCLUDED_PCT'].apply(lambda x: f"{x:.1f}%")

# Rearrange columns for final display
stats = stats[['TRANSACTIONS', 'INCLUDED_ON_CHAIN', 'INCLUDED_PCT', 'NOT_INCLUDED', 'NOT_INCLUDED_PCT']]

# Display the formatted table
print(stats)

# Number of top sources to display
top_n = 10
# Select top N sources by total transactions
top_sources = stats.sort_values(by='TRANSACTIONS', ascending=False).head(top_n)
# Ensure numeric data for plotting
transactions = top_sources['TRANSACTIONS'].replace(',', '', regex=True).astype(float).astype(int)
included = top_sources['INCLUDED_ON_CHAIN'].replace(',', '', regex=True).astype(float).astype(int)
not_included = top_sources['NOT_INCLUDED'].replace(',', '', regex=True).astype(float).astype(int)

# Prepare data
sources = top_sources.index
bar_width = 0.4
x = range(len(sources))

# Calculate the maximum value for the y-axis
y_max = max(included) + 10000

# Plot the bar chart
fig, ax = plt.subplots(figsize=(12, 8))

# Bar for included transactions (blue)
ax.bar([p - bar_width / 2 for p in x], included, width=bar_width, color='blue', label='Included On-Chain')

# Bar for not included transactions (orange)
ax.bar([p + bar_width / 2 for p in x], not_included, width=bar_width, color='orange', label='Not Included')

# Customize chart
ax.set_xlabel('Data Sources', fontsize=12)
ax.set_ylabel('Number of Transactions', fontsize=12)
ax.set_title(f'Transaction Statistics by Top {top_n} Data Sources', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(sources, rotation=45, ha='right', fontsize=10)
ax.set_ylim(0, y_max)  # Set y-axis limit to max included + 10,000
ax.legend()

# Add the max value to the y-axis
ax.set_yticks(list(ax.get_yticks()) + [y_max])

# Show the chart
plt.tight_layout()
plt.show()

# Count the occurrences of each source in the 'sources' column
source_counts = data_ori['sources'].value_counts()

# Calculate the relative frequency of each source
total_counts = source_counts.sum()
source_relative_frequencies = source_counts / total_counts

# Combine into a DataFrame for clarity
source_stats = pd.DataFrame({
    'Source': source_counts.index,
    'Count': source_counts.values,
    'Relative Frequency': source_relative_frequencies.values
})

# Display the resulting DataFrame
print(source_stats)