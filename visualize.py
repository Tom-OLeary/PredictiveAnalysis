"""Check for basic correlations to decide which stats to include"""

import sqlite3
import calculations
import matplotlib.pyplot as plt

from get_data import *

conn = sqlite3.connect('lahman2016.sqlite')

# Get Pitching Data
pitching_df = pd.read_sql(pitching_query, conn)

# Add Pitching Stats
pitching_df = calculations.add_fip(pitching_df)
pitching_df = calculations.add_h_a_per_game(pitching_df)
pitching_df = calculations.add_so_per_game(pitching_df)

'''Plotting Distribution of H_P'''
plt.hist(pitching_df['H_P'])
plt.xlabel('Hits Allowed')
plt.title('Distribution of Hits Allowed')

plt.show()

'''Creating bins for the hit column'''
pitching_df['hit_bins'] = pitching_df['H_P'].apply(calculations.assign_hit_bins)

'''Scatter Graph of Year vs Hits'''
plt.scatter(pitching_df['year'], pitching_df['H_P'], c=pitching_df['hit_bins'])
plt.title('Hits Scatter Plot')
plt.xlabel('Year')
plt.ylabel('Hits Allowed')

plt.show()

'''Filter for Hits > 120'''
pitching_df = pitching_df[pitching_df['H_P'] > 120]


'''Opp BA vs. Hits Allowed'''
plt.scatter(pitching_df['Opp_BA'], pitching_df['H_P'], edgecolor='black', linewidth=1,
            alpha=0.75, c=pitching_df['SO_P'], cmap='summer')

cbar = plt.colorbar()
cbar.set_label('Strikeouts')


plt.title('Opponent B.A. vs. Hits Allowed')
plt.xlabel('Opp BA')
plt.ylabel('Hits Allowed')

plt.tight_layout()

plt.show()


'''Scatter Subplots'''
fig = plt.figure(figsize=(12, 6))

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

'''FIP Vs. Hits Allowed'''
ax1.scatter(pitching_df['FIP'], pitching_df['H_P'], c='blue')
ax1.set_title('FIP vs. Hits Allowed')
ax1.set_ylabel('Hits Allowed')
ax1.set_xlabel('FIP')

'''Walks Vs. Hits Allowed'''
ax2.scatter(pitching_df['BB_P'], pitching_df['H_P'], c='red')
ax2.set_title('Walks vs. Hits Allowed')
ax2.set_xlabel('Walks')

plt.show()  # Little to no correlation


