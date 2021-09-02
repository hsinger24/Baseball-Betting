import pandas as pd
from bs4 import BeautifulSoup
import requests

from war_functions.pecota_tables import *

from cluster_luck_functions.cluster_luck_hitting import *
from cluster_luck_functions.cluster_luck_pitching import *
from cluster_luck_functions.cluster_luck_combined import *

from daily_adjustments.active_rosters import *
from daily_adjustments.BP_WAR import *
from daily_adjustments.todays_game_info import *
from daily_adjustments.starting_rotations_WAR import *
from daily_adjustments.adjusted_war_today import *

team_map = {
    'Giants' : 'San Francisco Giants',
    'Astros' : 'Houston Astros',
    'Brewers': 'Milwaukee Brewers',
    'Dodgers': 'Los Angeles Dodgers',
    'Rays' : 'Tampa Bay Rays',
    'Red Sox': 'Boston Red Sox',
    'White Sox': 'Chicago White Sox',
    'Padres': 'San Diego Padres',
    'Athletics': 'Oakland Athletics',
    'Yankees' : 'New York Yankees',
    'Mariners': 'Seattle Mariners',
    'Reds': 'Cincinnati Reds',
    'Blue Jays' : 'Toronto Blue Jays',
    'Mets' : 'New York Mets',
    'Phillies': 'Philadelphia Phillies',
    'Angels': 'Los Angeles Angels',
    'Braves': 'Atlanta Braves',
    'Cardinals': 'St. Louis Cardinals',
    'Tigers': 'Detroit Tigers',
    'Cubs': 'Chicago Cubs',
    'Indians': 'Cleveland Indians',
    'Nationals': 'Washington Nationals',
    'Rockies': 'Colorado Rockies',
    'Marlins': 'Miami Marlins',
    'Royals': 'Kansas City Royals',
    'Twins': 'Minnesota Twins',
    'Pirates': 'Pittsburgh Pirates',
    'Rangers': 'Texas Rangers',
    'Orioles': 'Baltimore Orioles',
    'Diamondbacks': 'Arizona Diamondbacks'
}

########## RETRIEVING NECESSARY DATA ##########

active_rosters = retrieve_all_active_rosters(file_name = None)
todays_games = retrieve_todays_games_info()
#retrieve_current_year_WAR()
current_year_WAR = load_current_year_WAR()
pt = load_combined_pecota_table()

########## GETTING CURRENT RUN DIFFERENTIAL WITH CURRENT CLUSTER LUCK ##########

def _retrieve_current_runs_scored():
    tables = pd.read_html('https://www.espn.com/mlb/stats/team')
    runs_scored_table = pd.merge(tables[0], tables[1], left_on = tables[0].index, right_on = tables[1].index)
    runs_scored_table.drop('key_0', axis = 1, inplace = True)
    runs_scored_table = runs_scored_table[['Team', 'GP', 'R']]
    runs_scored_table['Runs_162'] = runs_scored_table.R * (162.0/runs_scored_table.GP)
    return runs_scored_table

def _retrieve_current_runs_allowed():
    tables = pd.read_html('https://www.foxsports.com/mlb/team-stats?category=pitching&season=2021&seasonType=reg')
    runs_allowed_table = tables[1]
    runs_allowed_table = runs_allowed_table.iloc[:,[1,2,13]]
    runs_allowed_table.columns = ['Team', 'Games', 'Runs_Allowed']
    runs_allowed_table['Runs_Allowed_162'] = runs_allowed_table.Runs_Allowed * (162.0/runs_allowed_table.Games)
    runs_allowed_table['Team'] = runs_allowed_table.Team.apply(lambda x: team_map[x])
    return runs_allowed_table

def _calculate_current_run_differential():
    merged = pd.merge(_retrieve_current_runs_scored(), _retrieve_current_runs_allowed(), on = 'Team')
    merged = merged[['Team', 'Games', 'Runs_162', 'Runs_Allowed_162']]
    return merged

def _retrieve_current_cluster_luck_hitting():
    current_year_hitting = retrieve_historical_hitting_tables(2021, file_name = None)
    hitting_reg = load_linear_regression("data/hitting_regression.pickle")
    cluster_luck_hitting = calculate_predicted_cluster_luck_run_adjustment_hitting(hitting_reg, current_year_hitting)
    cluster_luck_hitting = cluster_luck_hitting[['Team', 'GP', 'run_adjust']]
    cluster_luck_hitting.columns = ['Team', 'Games', 'Offensive_Adjustment']
    return cluster_luck_hitting

def _retrieve_current_cluster_luck_pitching():
    current_year_pitching = retrieve_historical_pitching_tables(2021, file_name = None)
    pitching_reg = load_linear_regression('./data/pitching_regression.pickle')
    cluster_luck_pitching = calculate_predicted_cluster_luck_run_adjustment_pitching(pitching_reg, current_year_pitching)
    return cluster_luck_pitching

def _calculate_cluster_luck_tables():
    hitting = _retrieve_current_cluster_luck_hitting()
    pitching = _retrieve_current_cluster_luck_pitching()
    merged = pd.merge(hitting, pitching, on = 'Team')
    merged['Runs_Allowed'] = merged.RPG*merged.Games
    merged['Defensive_Adjustment'] = (
        (merged['predict'] - merged['HPR']) / merged['HPR'])*merged['Runs_Allowed']
    merged = merged[['Team', 'Offensive_Adjustment', 'Defensive_Adjustment']]
    merged['Team'] = merged.Team.apply(lambda x: team_map[x])
    return merged

def _calculate_cl_with_differential():
    cl  = _calculate_cluster_luck_tables()
    run_diff = _calculate_current_run_differential()
    merged = pd.merge(run_diff, cl, on = 'Team')
    return merged

#current_run_differential = _calculate_cl_with_differential()

########## MAKING WAR ADJUSTMENTS FOR ACTIVE ROSTER AND STARTING ROTATION ##########

#starting_rotations, failed_to_find_pitchers = retrieve_starting_rotations_WAR(pt, current_year_WAR)
#sp_adjustments = sp_adjustment(todays_games, starting_rotations, frac_season = 0.82)
overall_war_predictions_preseason = pd.read_csv('data/overall_war_predictions_preseason.csv')
active_roster_war, failed_to_find_players = active_roster_war_table(active_rosters, overall_war_predictions_preseason, current_year_WAR, pt, 2020, 0.82)
print(failed_to_find_players)
# Need to get WAR preseason predictions (not currently saved) before calling active roster adjustments