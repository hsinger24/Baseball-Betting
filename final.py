import pandas as pd
from sklearn.linear_model import LinearRegression
from bs4 import BeautifulSoup
from lxml import html
import requests
import re
import pprint

# projected war functions
from predictions.war_functions.get_active_roster import get_all_active_rosters
from predictions.war_functions.get_pecota_tables import get_combined_pecota_table
from predictions.war_functions.get_previous_year_war import get_combined_previous_year_war_table
from predictions.war_functions.get_overall_war_predictions import get_overall_war_predictions
from predictions.war_functions.get_final_war_table import get_final_war_table

# cluster luck functions
from predictions.cluster_luck_functions.get_cluster_luck_hitting import get_cluster_luck_hitting_table
from predictions.cluster_luck_functions.get_cluster_luck_pitching import get_cluster_luck_pitching_table
from predictions.cluster_luck_functions.get_combined_cluster_luck_table import merge_cluster_luck_tables

from predictions.get_final_win_percentage_table import get_win_percentage_predictions

from player_adjustments.get_starting_rotations import get_starting_rotations
from player_adjustments.get_todays_games_info import get_todays_games_info

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

# starting rotations to make adjustments on who is pitching on a given day
# failed_to_find_war_list is a list of pitchers where WAR was not found in the
#   pecota table due to some difference in the way the named was spelled
starting_rotations, failed_to_find_war_list = get_starting_rotations(
    pecota_table)

# get the starting pitchers, home team, away team, and lineup for today's games
todays_games_info = get_todays_games_info()
