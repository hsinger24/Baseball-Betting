import pandas as pd
from sklearn.linear_model import LinearRegression
from bs4 import BeautifulSoup
from lxml import html
import requests
import re
import pprint

# projected war functions
from war_functions.get_active_roster import get_all_active_rosters
from war_functions.get_pecota_tables import get_combined_pecota_table
from war_functions.get_previous_year_war import get_combined_previous_year_war_table
from war_functions.get_overall_war_predictions import get_overall_war_predictions
from war_functions.get_final_war_table import get_final_war_table

# cluster luck functions
from cluster_luck_functions.get_cluster_luck_hitting import get_cluster_luck_hitting_table
from cluster_luck_functions.get_cluster_luck_pitching import get_cluster_luck_pitching_table
from cluster_luck_functions.get_combined_cluster_luck_table import merge_cluster_luck_tables

from get_final_win_percentage_table import get_win_percentage_predictions

# projected war based off of last year and pecota
active_rosters = get_all_active_rosters()
pecota_table = get_combined_pecota_table()
previous_year_war_table = get_combined_previous_year_war_table()
projected_war_table = get_overall_war_predictions(active_rosters, pecota_table)
final_war_table = get_final_war_table(
    projected_war_table, previous_year_war_table)

# cluster luck tables
cluster_luck_hitting_table = get_cluster_luck_hitting_table()
cluster_luck_pitching_table = get_cluster_luck_pitching_table()
cluster_luck_combined_table = merge_cluster_luck_tables(
    cluster_luck_hitting_table, cluster_luck_pitching_table)

# merge cluster luck and war tables
win_percentage_predictions_table = get_win_percentage_predictions(
    cluster_luck_combined_table, final_war_table)

print(win_percentage_predictions_table)

# # In[8]:


# # Starting rotations

# team_list_link = ['https://www.lineups.com/mlb/depth-charts/arizona-diamondbacks', 'https://www.lineups.com/mlb/depth-charts/atlanta-braves',
#                   'https://www.lineups.com/mlb/depth-charts/baltimore-orioles', 'https://www.lineups.com/mlb/depth-charts/boston-red-sox',
#                   'https://www.lineups.com/mlb/depth-charts/chicago-cubs', 'https://www.lineups.com/mlb/depth-charts/chicago-white-sox',
#                   'https://www.lineups.com/mlb/depth-charts/cincinnati-reds', 'https://www.lineups.com/mlb/depth-charts/cleveland-indians',
#                   'https://www.lineups.com/mlb/depth-charts/colorado-rockies', 'https://www.lineups.com/mlb/depth-charts/detroit-tigers',
#                   'https://www.lineups.com/mlb/depth-charts/houston-astros', 'https://www.lineups.com/mlb/depth-charts/kansas-city-royals',
#                   'https://www.lineups.com/mlb/depth-charts/los-angeles-angels', 'https://www.lineups.com/mlb/depth-charts/los-angeles-dodgers',
#                   'https://www.lineups.com/mlb/depth-charts/miami-marlins', 'https://www.lineups.com/mlb/depth-charts/milwaukee-brewers',
#                   'https://www.lineups.com/mlb/depth-charts/minnesota-twins', 'https://www.lineups.com/mlb/depth-charts/new-york-mets',
#                   'https://www.lineups.com/mlb/depth-charts/new-york-mets', 'https://www.lineups.com/mlb/depth-charts/oakland-athletics',
#                   'https://www.lineups.com/mlb/depth-charts/philadelphia-phillies', 'https://www.lineups.com/mlb/depth-charts/pittsburgh-pirates',
#                   'https://www.lineups.com/mlb/depth-charts/san-diego-padres', 'https://www.lineups.com/mlb/depth-charts/san-francisco-giants',
#                   'https://www.lineups.com/mlb/depth-charts/seattle-mariners', 'https://www.lineups.com/mlb/depth-charts/st-louis-cardinals',
#                   'https://www.lineups.com/mlb/depth-charts/tampa-bay-rays', 'https://www.lineups.com/mlb/depth-charts/tampa-bay-rays',
#                   'https://www.lineups.com/mlb/depth-charts/toronto-blue-jays', 'https://www.lineups.com/mlb/depth-charts/washington-nationals']
# team_list = ['Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'Cubs', 'White Sox', 'Reds', 'Indians', 'Rockies',
#              'Tigers', 'Astros', 'Royals', 'Angels', 'Dodgers', 'Marlins', 'Brewers', 'Twins', 'Mets', 'Yankees',
#              'Athletics', 'Phillies', 'Pirates', 'Padres', 'Giants', 'Mariners', 'Cardinals', 'Rays', 'Rangers',
#              'Blue Jays', 'Nationals']

# starting_rotations = {}
# regex = r'^\S+\s\S+'
# l = 0
# for i in team_list_link:
#     tables = pd.read_html(i)
#     table = tables[1]
#     table['Position'] = table['Position'].astype('string')
#     subset = table[table['Position'] == 'Rotation  SP']
#     subset.drop('Position', axis=1, inplace=True)
#     subset.reset_index(inplace=True)
#     subset.drop('index', axis=1, inplace=True)
#     sp_list = list(subset.iloc[0, :])
#     sp = []
#     for j in sp_list:
#         pitch = re.findall(regex, j)
#         if pitch:
#             sp.append(pitch[0])
#     starting_rotations.update({team_list[l]: sp})
#     l = l+1


# # In[61]:


# starting_rotations_tables = {}
# z = 0
# for i in team_list:
#     table = pd.DataFrame(columns=['Name', 'WAR'])
#     k = 0
#     for j in starting_rotations[i]:
#         table.loc[k, 'Name'] = j
#         try:
#             war = pecota[pecota['name'] == j]['war_162'].iloc[0]
#             table.loc[k, 'WAR'] = war
#         except:
#             table.loc[k, 'WAR'] = 0
#             print(j)
#             z += 1
#         k = k+1
#     starting_rotations_tables[i] = table
# print(z)


# # In[63]:


# starting_rotations_tables['Cubs']


# # In[ ]:


# # In[ ]:
