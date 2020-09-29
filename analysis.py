"""Data Analysis: Dependent Variable = hit_event"""

import sqlite3
import matplotlib.pyplot as plt
import pickle
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.tree import DecisionTreeClassifier

from get_data import *
import calculations
from models import *
from grids import *

conn = sqlite3.connect('lahman2016.sqlite')

'''DataFrames'''
pitching_df = pd.read_sql(pitching_query, conn)
batting_df = pd.read_sql(batting_query, conn)
data_df = pd.DataFrame()

'''Event Logs'''
event_df = get_events()

'''Add Categories'''
event_df = calculations.add_year_label(event_df)
event_df = calculations.add_matchups(event_df)
event_df = calculations.add_dominant_arm(event_df)

pitching_df = calculations.add_fip(pitching_df)
pitching_df = calculations.add_h_a_per_game(pitching_df)
pitching_df = calculations.add_so_per_game(pitching_df)
pitching_df = calculations.add_phr_log5(pitching_df)

batting_df = calculations.add_hits_per_game(batting_df)
batting_df = calculations.add_bat_singles(batting_df)
batting_df = calculations.add_single_log5(batting_df)
batting_df = calculations.add_double_log5(batting_df)
batting_df = calculations.add_triple_log5(batting_df)
batting_df = calculations.add_hr_log5(batting_df)

print(pitching_df.head())

'''Convert year Value to String'''
df_list = [event_df, batting_df, pitching_df]
for i in df_list:
    i['year'] = i['year'].astype('str')

'''Merge DataFrames'''
event_df = pd.merge(event_df, batting_df, how='left', on=['bat_id', 'year'])
event_df = pd.merge(event_df, pitching_df, how='left', on=['pit_id', 'year'])
pd.set_option('display.max_columns', 36)
# print("pitching", event_df.isnull().sum(axis=0).tolist())

event_df.replace([np.inf, -np.inf], np.nan, inplace=True)
event_df.replace(r'\s+', np.nan, regex=True, inplace=True)
event_df.dropna(inplace=True)

'''Filter for Hits > 120'''
event_df = event_df[event_df['H_P'] > 120]

'''Create Hit Type Dictionary'''
hit_count = {}
for i, row in event_df.iterrows():
    player_id = row['pit_id']
    year = row['year']
    event_type = row['event_cd']
    count = 1
    if player_id in hit_count:
        if event_type == 2:
            hit_count[player_id]['outs'] = hit_count[player_id]['outs'] + count
        elif event_type == 20:
            hit_count[player_id]['singles_a'] = hit_count[player_id]['singles_a'] + count
        elif event_type == 21:
            hit_count[player_id]['doubles_a'] = hit_count[player_id]['doubles_a'] + count
        elif event_type == 22:
            hit_count[player_id]['triples_a'] = hit_count[player_id]['triples_a'] + count
    else:
        hit_count[player_id] = {}
        hit_count[player_id]['outs'] = 0
        hit_count[player_id]['singles_a'] = 0
        hit_count[player_id]['doubles_a'] = 0
        hit_count[player_id]['triples_a'] = 0
        if event_type == 2:
            hit_count[player_id]['outs'] = count
        elif event_type == 20:
            hit_count[player_id]['singles_a'] = count
        elif event_type == 21:
            hit_count[player_id]['doubles_a'] = count
        elif event_type == 22:
            hit_count[player_id]['triples_a'] = count
hit_count_df = pd.DataFrame.from_dict(hit_count, orient='index')

'''Add column for pit_id'''
hit_count_df['pit_id'] = hit_count_df.index

'''Add Event Probabilities to main DataFrame'''
event_df = pd.merge(event_df, hit_count_df, how='left', on=['pit_id'])
event_df = calculations.add_psingle_log5(event_df)
event_df = calculations.add_pdouble_log5(event_df)
event_df = calculations.add_ptriple_log5(event_df)
event_df = calculations.add_pbs_event(event_df)
event_df = calculations.add_pbd_event(event_df)
event_df = calculations.add_pbt_event(event_df)
event_df = calculations.add_pbhr_event(event_df)
event_df = calculations.add_hit_event(event_df)

'''K-Means Clustering'''
attributes = ['batters_faced', 'balls_ct', 'strikes_ct', 'singles', 'doubles', 'triples', 'prob1', 'prob2', 'prob3',
              'prob4', 'HR_P', 'singles_a', 'doubles_a', 'triples_a', 'HR', 'AB', 'H_P', 'ERA',
              'Opp_BA', 'so_pg', 'p_prob1', 'p_prob2', 'p_prob3', 'p_prob4',
              'd_event', 't_event', 's_event', 'hr_event', 'ha_pg']
data_attributes = event_df[attributes]
print(event_df.head())

'''Silhouette Score Dictionary'''
s_score_dict = {}
for i in range(2, 11):
    km = KMeans(n_clusters=i, random_state=1)
    l = km.fit_predict(data_attributes)
    s_s = metrics.silhouette_score(data_attributes, l, sample_size=1000)
    s_score_dict[i] = [s_s]

print(s_score_dict)  # Use 2 Clusters

'''Create K-Means Model and determine Euclidian distances for each data point'''
kmeans_model = KMeans(n_clusters=2, random_state=1)
distances = kmeans_model.fit_transform(data_attributes)

'''Create Scatter Plot using labels from K-Means Model as color'''
labels = kmeans_model.labels_

plt.scatter(distances[:, 0], distances[:, 1], c=labels)
plt.title('KMeans Clusters')

plt.show()

'''Add labels from K-Means Model to DataFrame and attributes list'''
event_df['labels'] = labels
attributes.append('labels')

print(event_df.head())


'''Plot Distribution of Hit Events'''
plt.hist(event_df['hit_event'])
plt.xlabel('Probability of Hit')
plt.title('Distribution of Hit Event')

plt.show()

event_df['hit_event_bin'] = event_df['hit_event'].apply(calculations.assign_hit_event_bins)

event_df = event_df[
    ['batters_faced', 'balls_ct', 'strikes_ct', 'singles', 'doubles', 'triples', 'prob1', 'prob2', 'prob3',
     'prob4', 'HR_P', 'singles_a', 'doubles_a', 'triples_a', 'HR', 'AB', 'H_P', 'ERA',
     'Opp_BA', 'so_pg', 'p_prob1', 'p_prob2', 'p_prob3', 'p_prob4',
     'd_event', 't_event', 's_event', 'hr_event', 'ha_pg', 'labels', 'hit_event_bin']]

'''Split data DataFrame into train and test sets'''
X_train, X_test, Y_train, Y_test = prepare_variables(event_df, 'hit_event_bin')

'''Testing Models'''
grid_search(X_train, Y_train, X_test, Y_test, 'decisiontree', DecisionTreeClassifier(), decision_tree_param)

model_list = [LinearRegression(normalize=True), RidgeCV(alphas=(0.01, 0.1, 1.0, 10.0), normalize=True)]
model_names = ['Linear Regression ', 'Ridge ']

# Print Score and MAE
for model, name in zip(model_list, model_names):
    get_score(model, X_train, Y_train, X_test, Y_test, name)


'''Save Model'''
# filename = 'final_model.sav'
# pickle.dump(linear_regression, open(filename, 'wb'))
