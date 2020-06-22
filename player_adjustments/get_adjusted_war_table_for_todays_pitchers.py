# sp_adjust_dict = {}
# i=0
# for game in games:
#     sp_home = game['home_team']['starting_pitcher']
#     sp_home_team = game['home_team']['team_name']
#     sp_away = game['away_team']['starting_pitcher']
#     sp_away_team = game['away_team']['team_name']

#     home_table = starting_rotations_tables[sp_home_team]
#     away_table = starting_rotations_tables[sp_away_team]

#     rotation_WAR_home = home_table.WAR.sum()
#     pitcher_WAR_home = home_table[home_table['Name'] == sp_home]['WAR'].iloc[0] * 5
#     WAR_diff_home = pitcher_WAR_home - rotation_WAR_home

#     rotation_WAR_away = away_table.WAR.sum()
#     pitcher_WAR_away = away_table[away_table['Name'] == sp_away]['WAR'].iloc[0] * 5
#     WAR_diff_away = pitcher_WAR_away - rotation_WAR_away


#   sp_adjust_dict.update({i: {'sp_home': sp_home, 'sp_home_team': sp_home_team, 'sp_home_WAR':pitcher_WAR_home,
#                               'sp_rotation_WAR_home': rotation_WAR_home, 'home_diff': WAR_diff_home, 'sp_away': sp_away,
#                              'sp_away_team': sp_away_team, 'sp_away_WAR': pitcher_WAR_away, 'sp_rotation_WAR_away':
#                               rotation_WAR_away, 'away_diff': WAR_diff_away}})
#     i = i + 1
