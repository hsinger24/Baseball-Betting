import pandas as pd
from sklearn.linear_model import LinearRegression
from bs4 import BeautifulSoup
from lxml import html
import requests
import re
import pprint

from get_active_roster import get_all_active_rosters
from get_pecota_tables import get_combined_pecota_table
from get_previous_year_war import get_combined_previous_year_war_table
from get_overall_war_predictions import get_overall_war_predictions
from get_final_war_table import get_final_war_table

active_rosters = get_all_active_rosters()
pecota_table = get_combined_pecota_table()
previous_year_war_table = get_combined_previous_year_war_table()
projected_war_table = get_overall_war_predictions(active_rosters, pecota_table)
final_war_table = get_final_war_table(
    projected_war_table, previous_year_war_table)

print(final_war_table)

# # In[6]:


# # Cluster luck

# # Historical hitting table (2017-2019)
# espn_list = ['https://www.espn.com/mlb/stats/team/_/stat/batting', 'https://www.espn.com/mlb/stats/team/_/stat/batting/season/2018/seasontype/2',
#              'https://www.espn.com/mlb/stats/team/_/stat/batting/season/2017/seasontype/2']
# espn_table = pd.DataFrame()
# for i in espn_list:
#     dfs = pd.read_html(i)
#     table = pd.concat([dfs[0], dfs[1]], axis=1)
#     espn_table = espn_table.append(table)
# espn_table.sort_values(by=['HR'], inplace=True, ascending=False)
# espn_table['ISO'] = (espn_table['2B']+2*espn_table['3B'] +
#                      3*espn_table['HR']) / espn_table['AB']
# espn_table['HPR'] = espn_table['H'] / espn_table['R']

# # Linear Regression for Hitting HPR
# X_hitting = espn_table.loc[:, ['OBP', 'ISO', 'SLG']]
# Y_hitting = espn_table.HPR
# lr_hitting = LinearRegression()
# lr_hitting.fit(X_hitting, Y_hitting)

# # Creating 2019 Hitting Table With CL adjustments
# dfs_hitting_2019 = pd.read_html(
#     'https://www.espn.com/mlb/stats/team/_/stat/batting')
# hitting_2019 = pd.concat([dfs_hitting_2019[0], dfs_hitting_2019[1]], axis=1)
# hitting_2019['ISO'] = (hitting_2019['2B']+2*hitting_2019['3B'] +
#                        3*hitting_2019['HR']) / hitting_2019['AB']
# hitting_2019['HPR'] = hitting_2019['H'] / hitting_2019['R']
# hitting_2019_X = hitting_2019.loc[:, ['OBP', 'ISO', 'SLG']]
# hitting_2019['predict'] = lr_hitting.predict(hitting_2019_X)
# hitting_2019['run_adjust'] = (
#     (hitting_2019['HPR'] - hitting_2019['predict'])/hitting_2019['HPR'])*hitting_2019['R']
# team_list_hitting = ['Astros', 'Twins', 'Red Sox', 'Yankees', 'Rockies', 'Nationals', 'Pirates', 'White Sox', 'Braves', 'Dodgers', 'Mets', 'Rays', 'Cubs', 'Diamondbacks',
#                      'Indians', 'Athletics', 'Rangers', 'Angels', 'Royals', 'Brewers', 'Orioles', 'Phillies', 'Cardinals', 'Reds', 'Marlins', 'Tigers', 'Giants', 'Padres', 'Mariners', 'Blue Jays']
# hitting_2019['Team'] = team_list_hitting

# # Historical Pitching Table (2017-2019)


# def table_maker(link_list, prior_year):
#     table_list = []
#     for i in link_list:
#         dfs = pd.read_html(i)
#         df = dfs[0]
#         df.drop(['Last 3', 'Last 1', 'Home', 'Away',
#                  prior_year], axis=1, inplace=True)
#         table_list.append(df)
#     df1 = pd.merge(left=table_list[0], right=table_list[1], on='Team')
#     df2 = pd.merge(left=df1, right=table_list[2], on='Team')
#     df2.drop(['Rank_x', 'Rank_y', 'Rank'], axis=1, inplace=True)
#     df3 = pd.merge(left=df2, right=table_list[3], on='Team')
#     pitching_table = pd.merge(left=df3, right=table_list[4], on='Team')
#     pitching_table.drop(['Rank_x', 'Rank_y'], axis=1, inplace=True)
#     pitching_table.columns = ['Team', 'SLG', 'OBP', 'ISO', 'RPG', 'HPG']
#     pitching_table['HPR'] = pitching_table.HPG / pitching_table.RPG
#     return pitching_table


# link_list_2019 = ['https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date=2019-10-31', 'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date=2019-10-31',
#                   'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date=2019-10-31', 'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date=2019-10-31', 'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date=2019-10-31']
# table_2019 = table_maker(link_list_2019, '2018')
# link_list_2018 = ['https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date=2018-10-29',
#                   'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date=2018-10-29']
# link_list_2017 = ['https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date=2017-11-02',
#                   'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date=2017-11-02']
# table_2018 = table_maker(link_list_2018, '2017')
# table_2017 = table_maker(link_list_2017, '2016')
# t1 = table_2019.append(table_2018)
# pitching_data = t1.append(table_2017)

# # Linear Regression for Pitching
# X_pitching = pitching_data.loc[:, ['SLG', 'OBP', 'ISO']]
# Y_pitching = pitching_data.HPR
# lr_pitching = LinearRegression()
# lr_pitching.fit(X_pitching, Y_pitching)

# # Creating 2019 Pitching Table With CL Adjustments
# pitching_2019_x = table_2019.loc[:, ['SLG', 'OBP', 'ISO']]
# table_2019['predict'] = lr_pitching.predict(pitching_2019_x)
# table_2019['R'] = table_2019.RPG*162
# table_2019['Run_Adjust'] = (
#     (table_2019['predict'] - table_2019['HPR'])/table_2019['HPR'])*table_2019['R']
# team_list = ['Dodgers', 'Rays', 'Cardinals', 'Astros', 'Athletics', 'Reds', 'Nationals', 'Cubs', 'Mets', 'Indians', 'Braves', 'Twins', 'Brewers', 'Giants', 'Padres',
#              'Red Sox', 'Diamondbacks', 'Yankees', 'Marlins', 'Blue Jays', 'White Sox', 'Phillies', 'Royals', 'Angels', 'Rangers', 'Mariners', 'Pirates', 'Tigers', 'Rockies', 'Orioles']
# table_2019['Team'] = team_list

# # Merging 2019 Hitting and Pitching with CL Adjustments
# cluster_final = pd.merge(hitting_2019, table_2019, on='Team')
# drop_list = ['RK', 'GP', 'AB', 'H', '2B', '3B', 'HR', 'RBI', 'TB',
#              'BB', 'SO', 'SB', 'AVG', 'OBP_x', 'SLG_x', 'OPS', 'ISO_x', 'HPR_x',
#              'predict_x', 'SLG_y', 'OBP_y', 'ISO_y', 'RPG', 'HPG',
#              'HPR_y', 'predict_y', ]
# cluster_final.drop(drop_list, axis=1, inplace=True)
# cluster_final.columns = [
#     'Team', 'Runs', 'Offensive_Adjustment', 'Runs_Allowed', 'Defensive_Adjustment']
# #cluster_final['Adjusted_Differential'] = cluster_final.Runs + cluster_final.Offensive_Adjustment + cluster_final.Defensive_Adjustment - cluster_final.Runs_Allowed
# cluster_final['Defensive_Adjustment'] = -cluster_final['Defensive_Adjustment']
# cluster_final['Adjusted_Runs_Scored'] = cluster_final.Runs + \
#     cluster_final.Offensive_Adjustment
# cluster_final['Adjusted_Runs_Allowed'] = cluster_final.Runs_Allowed + \
#     cluster_final.Defensive_Adjustment


# # In[7]:


# # Final Merge to create base Win % Adjustments
# final = pd.merge(cluster_final, final_WAR_table, on='Team')
# display(final.columns)
# drop_list_final = ['Runs', 'Offensive_Adjustment', 'Runs_Allowed',
#                    'Defensive_Adjustment',
#                    '2020', '2019', ]
# final.drop(drop_list_final, axis=1, inplace=True)
# # Using Pythagorean Linear Regression to Predict Win %
# final['Win_Percentage'] = .5 + 0.000683 * \
#     (final.Adjusted_Runs_Scored + final.Run_Change - final.Adjusted_Runs_Allowed)
# display(final)


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
