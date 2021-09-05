########## IMPORTS ##########
import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime as dt

from war_functions.pecota_tables import *

from cluster_luck_functions.cluster_luck_hitting import *
from cluster_luck_functions.cluster_luck_pitching import *
from cluster_luck_functions.cluster_luck_combined import *

from daily_adjustments.active_rosters import *
from daily_adjustments.BP_WAR import *
from daily_adjustments.todays_game_info import *
from daily_adjustments.starting_rotations_WAR import *
from daily_adjustments.adjusted_war_today import *

from odds_and_other_projections import *

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
    'Diamondbacks': 'Arizona Diamondbacks',
    'D-backs' : 'Arizona Diamondbacks'
}
########## SETTING NECESSARY PARAMETERS ##########

frac_season = 0.82
current_year = 2020
capital = int(input('Hank, please input your current capital: '))
kelly = 10
today = str(dt.date.today()).replace('-', '')

########## RETRIEVING NECESSARY DATA ##########

active_rosters = retrieve_all_active_rosters(file_name = None)
todays_games = retrieve_todays_games_info()
#retrieve_current_year_WAR()
current_year_WAR = load_current_year_WAR()
pt = load_combined_pecota_table()
odds = retrieve_odds()

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

current_run_differential = _calculate_cl_with_differential()
#print(current_run_differential)

# ########## MAKING WAR ADJUSTMENTS FOR ACTIVE ROSTER AND STARTING ROTATION ##########

starting_rotations, failed_to_find_pitchers = retrieve_starting_rotations_WAR(pt, current_year_WAR)
print(failed_to_find_pitchers)
sp_adjustments = sp_adjustment(todays_games, starting_rotations, frac_season = frac_season)
print(sp_adjustments)
overall_war_predictions_preseason = pd.read_csv('data/overall_war_predictions_preseason.csv')
active_roster_war, failed_to_find_players = active_roster_war_table(active_rosters, overall_war_predictions_preseason, current_year_WAR, pt, current_year, frac_season)
print(failed_to_find_players)
print(active_roster_war)

########## COMBINING ALL INPUTS TO GET TODAY'S WIN PERCENTAGE FOR EACH TEAM ##########

def todays_win_percentages(preseason_projections, current_run_differential, sp_adjustments, active_roster_war, frac_season):
    
    # Creating df, filling team column
    todays_projections = pd.DataFrame(columns = ['Team', 'Preseason_Projections', 'CY_Win_Pct', 'SP_Adjustment', 'Active_Roster_Adjustment', 'Today_Win_Pct'])
    todays_projections['Team'] = current_run_differential.Team
    for column in list(todays_projections.columns):
        if column != 'Team':
            todays_projections[column] = 0

    # Putting preseason projections into table
    preseason_projections['Team'] = preseason_projections.Team.apply(lambda x: team_map[x])
    for index, row in todays_projections.iterrows():
        team = row.Team
        preseason_win_pct = preseason_projections.loc[preseason_projections.Team==team, 'Win_Percentage'].values[0]
        todays_projections.loc[index, 'Preseason_Projections'] = preseason_win_pct
    
    # Putting current year win % into table
    current_run_differential['Adjusted_Runs_Scored'] = current_run_differential['Runs_162'] + current_run_differential['Offensive_Adjustment']
    current_run_differential['Adjusted_Runs_Allowed'] = current_run_differential['Runs_Allowed_162'] - current_run_differential['Defensive_Adjustment']
    current_run_differential['Win_Percentage'] = .5 + 0.000683 * \
        (current_run_differential.Adjusted_Runs_Scored - current_run_differential.Adjusted_Runs_Allowed)
    for index, row in todays_projections.iterrows():
        team = row.Team
        cy_win_pct = current_run_differential.loc[current_run_differential.Team==team, 'Win_Percentage'].values[0]
        todays_projections.loc[index, 'CY_Win_Pct'] = cy_win_pct
    # Putting SP Adjustment into tables
    for matchup in sp_adjustments:
        home_team = team_map[matchup['home_team']]
        away_team = team_map[matchup['away_team']]
        todays_projections.loc[todays_projections.Team==home_team, 'SP_Adjustment'] = matchup['home_adjustment']*10
        todays_projections.loc[todays_projections.Team==away_team, 'SP_Adjustment'] = matchup['away_adjustment']*10
    # Putting active roster adjustment into table
    for index, row in active_roster_war.iterrows():
        team_short = row.Team
        team_long = team_map[team_short]
        Run_difference = row.Run_difference
        todays_projections.loc[todays_projections.Team==team_long, 'Active_Roster_Adjustment'] = Run_difference
    # Getting today's win % based on inputs
    if frac_season>0.25:
        todays_projections['Today_Win_Pct'] = todays_projections.Preseason_Projections*(1.0-frac_season) + (todays_projections.CY_Win_Pct * frac_season) \
            + 0.000683 * (todays_projections.SP_Adjustment + todays_projections.Active_Roster_Adjustment)
    else:
        todays_projections['Today_Win_Pct'] = todays_projections.Preseason_Projections + \
            0.000683 * (todays_projections.SP_Adjustment + todays_projections.Active_Roster_Adjustment)

    return todays_projections

preseason_projections = pd.read_csv('data/preseason_projections.csv')
todays_win_percentages = todays_win_percentages(preseason_projections, current_run_differential, sp_adjustments, active_roster_war, frac_season)
print(todays_win_percentages)

########## TODAYS BETS ##########

def todays_bets(todays_games, todays_win_percentages, odds, capital, kelly):

    # Creating kelly calculator function
    def kelly_criterion_home():
        if home_diff<0:
            return 0
        else:
            p = home_prob
            q = 1-p
            ml = home_ml
            if ml>=0:
                b = (ml/100)
            if ml<0:
                b = (100/abs(ml))
            kc = ((p*b) - q) / b
            if (kc > 0.5) & (kc<0.6):
                return kc/(kelly+2)
            if (kc > 0.6) & (kc<0.7):
                return kc/(kelly+4)
            if kc > 0.7:
                return kc/(kelly+7)
            else:
                return kc/kelly
    def kelly_criterion_away():
        if away_diff<0:
            return 0
        else:
            p = away_prob
            q = 1-p
            ml = away_ml
            if ml>=0:
                b = (ml/100)
            if ml<0:
                b = (100/abs(ml))
            kc = ((p*b) - q) / b
            if (kc > 0.5) & (kc<0.6):
                return kc/(kelly+2)
            if (kc > 0.6) & (kc<0.7):
                return kc/(kelly+4)
            if kc > 0.7:
                return kc/(kelly+7)
            else:
                return kc/kelly

    # Creating data frame
    todays_bets = pd.DataFrame(columns = ['Home_Team', 'Away_Team', 'Home_Prob', 'Away_Prob', 'Home_ML', 'Away_ML', 
    'Home_ML_Prob', 'Away_ML_Prob', 'Home_Diff','Away_Diff', 'Home_KC', 'Away_KC', 'Home_Bet', 'Away_Bet'])

    # Formatting odds to match team name
    odds['Home_Team'] = odds.Home_Team.apply(lambda x: team_map[x])
    odds['Away_Team'] = odds.Away_Team.apply(lambda x: team_map[x])

    # Filling df with relevant info
    for game in todays_games:
        home_team = team_map[game['home_team']['team_name']]
        away_team = team_map[game['away_team']['team_name']]
        print(home_team)
        home_prob_orig = todays_win_percentages.loc[todays_win_percentages.Team==home_team, 'Today_Win_Pct'].values[0]
        away_prob_orig = todays_win_percentages.loc[todays_win_percentages.Team==away_team, 'Today_Win_Pct'].values[0]
        home_prob = home_prob_orig*(1-away_prob_orig)
        away_prob = away_prob_orig*(1-home_prob_orig)
        home_prob = home_prob/(home_prob+away_prob)
        home_prob = home_prob*1.08
        away_prob = 1 - home_prob
        home_ml = odds.loc[odds.Home_Team==home_team,'Home_Odds'].values[0]
        away_ml = odds.loc[odds.Away_Team==away_team, 'Away_Odds'].values[0]
        home_ml_prob = odds.loc[odds.Home_Team==home_team,'Home_Prob'].values[0]/100
        away_ml_prob = odds.loc[odds.Away_Team==away_team, 'Away_Prob'].values[0]/100
        home_diff = home_prob - home_ml_prob
        away_diff = away_prob - away_ml_prob
        home_kc = kelly_criterion_home()
        away_kc = kelly_criterion_away()
        home_bet = capital * home_kc
        away_bet = capital * away_kc
        series = pd.Series([home_team, away_team, home_prob, away_prob, home_ml, away_ml, home_ml_prob, away_ml_prob,
        home_diff, away_diff, home_kc, away_kc, home_bet, away_bet], index = todays_bets.columns)
        todays_bets = todays_bets.append(series, ignore_index = True)
    return todays_bets

todays_bets = todays_bets(todays_games = todays_games, todays_win_percentages = todays_win_percentages, odds = odds, capital = capital, kelly = kelly)
todays_bets.to_csv('past_bets/bets' + today + '.csv')
print(todays_bets)