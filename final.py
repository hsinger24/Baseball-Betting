'''
Project: MLB Baseball Betting Model
Authors: Henry Singer, Ryan Loutos, Ben Schulman
'''

# projected war functions
from predictions.war_functions.active_rosters import load_active_rosters, retrieve_all_active_rosters
from predictions.war_functions.pecota_tables import load_combined_pecota_table
from predictions.war_functions.war_table import retrieve_historical_combined_war_table, load_combined_war_table
from predictions.war_functions.war_projections import calculate_team_war_projections_table
from predictions.war_functions.final_war_table import calculate_final_war_table

# cluster luck functions
from predictions.cluster_luck_functions.get_cluster_luck_hitting import get_cluster_luck_hitting_table
from predictions.cluster_luck_functions.get_cluster_luck_pitching import get_cluster_luck_pitching_table
from predictions.cluster_luck_functions.get_combined_cluster_luck_table import merge_cluster_luck_tables

from predictions.get_final_win_percentage_table import get_win_percentage_predictions

from player_adjustments.get_starting_rotations import get_starting_rotations
from player_adjustments.get_todays_games_info import get_todays_games_info

import datetime as dt

curr_year = dt.date.today().year
last_year = curr_year - 1

# ------------- WAR -------------
# Retrieve Data
retrieve = True
if retrieve:
    retrieve_all_active_rosters()
    retrieve_historical_combined_war_table(last_year, file_path=f"data/war_table_{last_year}csv")

# Load Data
# projected war based off of last year and pecota
active_rosters = load_active_rosters()
pecota_table = load_combined_pecota_table()
previous_year_war_table = load_combined_war_table(file_path=f"data/war_table_{last_year}.csv")

# Calculate Results
projected_war_table = calculate_team_war_projections_table(active_rosters, pecota_table)
final_war_table = calculate_final_war_table(projected_war_table, previous_year_war_table)


# ------------- Cluster Luck -------------

# cluster luck tables
cluster_luck_hitting_table = get_cluster_luck_hitting_table()
cluster_luck_pitching_table = get_cluster_luck_pitching_table()
cluster_luck_combined_table = merge_cluster_luck_tables(
    cluster_luck_hitting_table, cluster_luck_pitching_table)

# merge cluster luck and war tables
win_percentage_predictions_table = get_win_percentage_predictions(
    cluster_luck_combined_table, final_war_table)

# starting rotations to make adjustments on who is pitching on a given day
# failed_to_find_war_list is a list of pitchers where WAR was not found in the
#   pecota table due to some difference in the way the named was spelled
starting_rotations, failed_to_find_war_list = get_starting_rotations(
    pecota_table)

# get the starting pitchers, home team, away team, and lineup for today's games
todays_games_info = get_todays_games_info()
