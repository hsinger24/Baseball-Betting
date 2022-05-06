##########IMPORTS AND PARAMETERS##########


# Imports
import pandas as pd
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

# Parameters
current_year = dt.date.today().year
today = str(dt.date.today()).replace('-', '')
today_date = dt.date.today()
yesterday = today_date - dt.timedelta(days=1)
yesterday_string = str(yesterday)
yesterday_string = yesterday_string.replace('-', '')
kelly = 10
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
    'Guardians' : 'Cleveland Guardians',
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

##########FUNCTIONS##########


def _retrieve_current_runs_scored():
    tables = pd.read_html('https://www.espn.com/mlb/stats/team')
    runs_scored_table = pd.merge(tables[0], tables[1], left_on = tables[0].index, right_on = tables[1].index)
    runs_scored_table.drop('key_0', axis = 1, inplace = True)
    runs_scored_table = runs_scored_table[['Team', 'GP', 'R']]
    runs_scored_table['Runs_162'] = runs_scored_table.R * (162.0/runs_scored_table.GP)
    return runs_scored_table

def _retrieve_current_runs_allowed():
    tables = pd.read_html(f'https://www.foxsports.com/mlb/team-stats?category=pitching&season={dt.date.today().year}&seasonType=reg')
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
    current_year_hitting = retrieve_historical_hitting_tables(current_year, file_name = None)
    hitting_reg = load_linear_regression("data/hitting_regression.pickle")
    cluster_luck_hitting = calculate_predicted_cluster_luck_run_adjustment_hitting(hitting_reg, current_year_hitting)
    cluster_luck_hitting = cluster_luck_hitting[['Team', 'GP', 'run_adjust']]
    cluster_luck_hitting.columns = ['Team', 'Games', 'Offensive_Adjustment']
    cluster_luck_hitting['Offensive_Adjustment'] = cluster_luck_hitting.Offensive_Adjustment * (162.0/cluster_luck_hitting.Games)
    return cluster_luck_hitting

def _retrieve_current_cluster_luck_pitching():
    current_year_pitching = retrieve_historical_pitching_tables(current_year, file_name = None)
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

def _calculate_frac_season():
    df = _retrieve_current_cluster_luck_hitting()
    df['Frac_Season'] = df.Games/162.0
    frac_season = df.Frac_Season.mean()
    return frac_season

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
        if todays_win_percentages.loc[todays_win_percentages.Team==home_team, 'SP_Adjustment'].values[0]==0:
            continue
        if todays_win_percentages.loc[todays_win_percentages.Team==away_team, 'SP_Adjustment'].values[0]==0:
            continue
        home_prob_orig = todays_win_percentages.loc[todays_win_percentages.Team==home_team, 'Today_Win_Pct'].values[0]
        away_prob_orig = todays_win_percentages.loc[todays_win_percentages.Team==away_team, 'Today_Win_Pct'].values[0]
        home_prob = home_prob_orig*(1-away_prob_orig)
        away_prob = away_prob_orig*(1-home_prob_orig)
        home_prob = home_prob/(home_prob+away_prob)
        home_prob = home_prob*1.08
        away_prob = 1 - home_prob
        try:
            home_ml = odds.loc[odds.Home_Team==home_team,'Home_Odds'].values[0]
        except:
            continue
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

def calculate_payoff(row):
    if row.Home_KC>0:
        if row.Home_ML>0:
            payoff = (row.Home_ML/100)*row.Home_Bet
        if row.Home_ML<0:
            payoff = row.Home_Bet/((abs(row.Home_ML)/100))
    elif row.Away_KC>0:
        if row.Away_ML>0:
            payoff = (row.Away_ML/100)*row.Away_Bet
        if row.Away_ML<0:
            payoff = row.Away_Bet/((abs(row.Away_ML)/100))
    return payoff

def calculate_yesterdays_bets_results(yesterday_string, yesterdays_capital):
    
    # Getting yesterdays results from CBS
    link = 'https://www.cbssports.com/mlb/scoreboard/' + yesterday_string + '/'
    tables = pd.read_html(link)
    results_table = pd.DataFrame(columns = ['Home_Team', 'Away_Team', 'Winner'])
    for table in tables:
        if list(table.columns) == ['Unnamed: 0', 'R', 'H', 'E']:

            # Getting team names
            team_away_list = table.iloc[0,0].split(' ')
            del team_away_list[-2:]
            if len(team_away_list) == 2:
                team_away = team_away_list[0] + ' ' + team_away_list[1]
            else:
                team_away = team_away_list[0]
            team_home_list = table.iloc[1,0].split(' ')
            del team_home_list[-2:]
            if len(team_home_list) == 2:
                team_home = team_home_list[0] + ' ' + team_home_list[1]
            else:
                team_home = team_home_list[0]
            
            # Getting score and determining winner
            runs_away = table.iloc[0,1]
            runs_home = table.iloc[1,1]
            if runs_away>runs_home:
                winner = team_away
            else:
                winner = team_home

            # Appending to results table
            series = pd.Series([team_home, team_away, winner], index = results_table.columns)
            results_table = results_table.append(series, ignore_index = True)        
        else:
            continue
    for column in list(results_table.columns):
        results_table[column] = results_table[column].apply(lambda x: team_map[x])

    # Reading in yesterdays bets and creating tracker columns
    yesterdays_bets = pd.read_csv('past_bets/base/bets_' + yesterday_string + '.csv', index_col = 0)
    yesterdays_bets['Won'] = 0
    yesterdays_bets['Money_Tracker'] = 0
    yesterdays_bets = yesterdays_bets[(yesterdays_bets.Home_Bet>0) | (yesterdays_bets.Away_Bet>0)]
    yesterdays_bets.reset_index(drop = True, inplace = True)
    for index,row in yesterdays_bets.iterrows():
        payoff = calculate_payoff(row)
        # For postponed games
        if (row.Home_Team not in results_table['Winner'].values) & (row.Away_Team not in results_table['Winner'].values):
            yesterdays_bets.loc[index, 'Won'] = -1
            if index == 0:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_capital
            else:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_bets.loc[(index-1), 'Money_Tracker']
            continue
        # For doubleheaders
        if (row.Home_Team in results_table['Winner'].values) & (row.Away_Team  in results_table['Winner'].values):
            yesterdays_bets.loc[index, 'Won'] = -1
            if index == 0:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_capital
            else:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_bets.loc[(index-1), 'Money_Tracker']
            continue
        elif (list(results_table['Winner'].values).count(row.Home_Team) > 1) | (list(results_table['Winner'].values).count(row.Away_Team) > 1):
            yesterdays_bets.loc[index, 'Won'] = -1
            if index == 0:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_capital
            else:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_bets.loc[(index-1), 'Money_Tracker']
            continue
        else:
            pass
        if row.Home_Bet>0:
            if row.Home_Team in results_table['Winner'].values:
                yesterdays_bets.loc[index, 'Won'] = 1
        if row.Away_Bet>0:
            if row.Away_Team in results_table['Winner'].values:
                yesterdays_bets.loc[index, 'Won'] = 1
        if yesterdays_bets.loc[index, 'Won'] == 1:
            if index == 0:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_capital + payoff
            else:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_bets.loc[(index-1), 'Money_Tracker'] + payoff
        else:
            if index == 0:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_capital - row.Home_Bet - row.Away_Bet
            else:
                yesterdays_bets.loc[index, 'Money_Tracker'] = yesterdays_bets.loc[(index-1), 'Money_Tracker'] - row.Home_Bet - row.Away_Bet
    yesterdays_bets['Date'] = today
    return yesterdays_bets

def calculate_bets_external(capital_538):

    # Getting odds and 538 data in one place
    data = retrieve_538()
    odds = retrieve_odds()
    merged = pd.merge(data, odds, on = 'Home_Team')
    merged = merged[['Date', 'Away_Team_x', 'Home_Team', 'Away_Prob_x', 'Home_Prob_x', 'Home_Odds', 'Away_Odds',
        'Home_Prob_y', 'Away_Prob_y']]
    merged.columns = ['Date', 'Away_Team', 'Home_Team', 'Away_Prob_538', 'Home_Prob_538', 'Home_Odds', 'Away_Odds',
        'Home_Prob_Odds', 'Away_Prob_Odds']

    # Formatting data
    merged['Home_Prob_538'] = merged.Home_Prob_538.str.strip('%')
    merged['Away_Prob_538'] = merged.Away_Prob_538.str.strip('%')
    merged['Home_Prob_538'] = merged.Home_Prob_538.astype('float') / 100.0
    merged['Away_Prob_538'] = merged.Away_Prob_538.astype('float') / 100.0
    merged['Home_Prob_Odds'] = merged.Home_Prob_Odds / 100.0
    merged['Away_Prob_Odds'] = merged.Away_Prob_Odds / 100.0
    current_day = dt.date.today().day
    merged['Date_Day'] = merged.Date.dt.day
    merged = merged[merged.Date_Day == current_day]
    merged.drop_duplicates(inplace = True, subset = ['Home_Team', 'Away_Team'])
    merged.drop(['Date_Day'], axis = 1, inplace = True)

    # Defining KC calculator function
    def kc(row, kelly, Home):
        if Home:
            diff = row.Home_Prob_538 - row.Home_Prob_Odds
            if diff<0:
                return 0
            else:
                p = row.Home_Prob_538
                q = 1-p
                ml = row.Home_Odds
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
        if not Home:
            diff = row.Away_Prob_538 - row.Away_Prob_Odds
            if diff<0:
                return 0
            else:
                p = row.Away_Prob_538
                q = 1-p
                ml = row.Away_Odds
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
        
    # Creating bets
    merged['Home_KC_538'] = merged.apply(kc, axis = 1, kelly = 10, Home = True)
    merged['Away_KC_538'] = merged.apply(kc, axis = 1, kelly = 10, Home = False)
    merged['Bet_538'] = merged.apply(lambda x: capital_538 * x.Home_KC_538 if x.Home_KC_538>0
            else capital_538 * x.Away_KC_538, axis = 1)
    
    # Changing 538 to Guardians
    merged['Home_Team'] = merged.Home_Team.apply(lambda x: 'Guardians' if x == '538' else x)
    merged['Away_Team'] = merged.Away_Team.apply(lambda x: 'Guardians' if x == '538' else x)

    return merged

def calculate_yesterdays_bet_results_external(yesterday_string, yesterdays_capital_538):
    
    # Function to calculate potential payoffs
    def calculate_payoff_external(row):
        if row.Bet_538<=0:
            payoff = 0
        else:
            if row.Home_KC_538>0:
                if row.Home_Odds>0:
                    payoff = (row.Home_Odds/100)*row.Bet_538
                if row.Home_Odds<0:
                    payoff = row.Bet_538/((abs(row.Home_Odds)/100))
            if row.Away_KC_538>0:
                if row.Away_Odds>0:
                    payoff = (row.Away_Odds/100)*row.Bet_538
                if row.Away_Odds<0:
                    payoff = row.Bet_538/((abs(row.Away_Odds)/100))
        return payoff

    # Getting yesterday's results from CBS
    link = 'https://www.cbssports.com/mlb/scoreboard/' + yesterday_string + '/'
    tables = pd.read_html(link)
    results_table = pd.DataFrame(columns = ['Home_Team', 'Away_Team', 'Winner'])
    for table in tables:
        if list(table.columns) == ['Unnamed: 0', 'R', 'H', 'E']:
            # Getting team names
            team_away_list = table.iloc[0,0].split(' ')
            del team_away_list[-2:]
            if len(team_away_list) == 2:
                team_away = team_away_list[0] + ' ' + team_away_list[1]
            else:
                team_away = team_away_list[0]
            team_home_list = table.iloc[1,0].split(' ')
            del team_home_list[-2:]
            if len(team_home_list) == 2:
                team_home = team_home_list[0] + ' ' + team_home_list[1]
            else:
                team_home = team_home_list[0]
            # Getting score and determining winner
            runs_away = table.iloc[0,1]
            runs_home = table.iloc[1,1]
            if runs_away>runs_home:
                winner = team_away
            else:
                winner = team_home
            # Appending to results table
            series = pd.Series([team_home, team_away, winner], index = results_table.columns)
            results_table = results_table.append(series, ignore_index = True)        
        else:
            continue
    for column in list(results_table.columns):
        results_table[column] = results_table[column].apply(lambda x: team_map[x])

    # Reading in yesterdays bets and creating tracker columns
    yesterdays_bets = pd.read_csv('past_bets/external/bets_' + yesterday_string + '.csv', index_col = 0)
    yesterdays_bets = yesterdays_bets[(yesterdays_bets.Home_Team != '538') & (yesterdays_bets.Away_Team != '538')]
    yesterdays_bets['Home_Team'] = yesterdays_bets['Home_Team'].apply(lambda x: team_map[x])
    yesterdays_bets['Away_Team'] = yesterdays_bets['Away_Team'].apply(lambda x: team_map[x])
    yesterdays_bets = yesterdays_bets[yesterdays_bets.Bet_538>0]
    yesterdays_bets.reset_index(drop = True, inplace = True)
    yesterdays_bets['Won_538'] = 0
    yesterdays_bets['Tracker_538'] = 0
    for index, row in yesterdays_bets.iterrows():
        home_team = row.Home_Team
        away_team = row.Away_Team
        payoff_538 = calculate_payoff_external(row)
        # Signifying win, loss, or other
        if row.Bet_538>0:
            # Normal bets
            if (row.Home_KC_538>0) & (home_team in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_538'] = 1
            elif (row.Away_KC_538>0) & (away_team in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_538'] = 1
            else:
                yesterdays_bets.loc[index, 'Won_538'] = 0
            # Postponed games
            if (home_team not in results_table['Winner'].values) & (away_team not in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_538'] = -1
            # Double headers
            if (home_team in results_table['Winner'].values) & (away_team in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_538'] = -1
            elif (list(results_table['Winner'].values).count(home_team) > 1) | (list(results_table['Winner'].values).count(away_team) > 1):
                yesterdays_bets.loc[index, 'Won_538'] = -1
        # Games that weren't bet on
        else:
            yesterdays_bets.loc[index, 'Won_538'] = -1
        # Updating tracker
        if yesterdays_bets.loc[index, 'Won_538'] == 1:
            if index == 0:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_capital_538 + payoff_538
            else:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_bets.loc[(index-1), 'Tracker_538'] + payoff_538
        elif yesterdays_bets.loc[index, 'Won_538'] == -1:
            if index == 0:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_capital_538
            else:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_bets.loc[(index-1), 'Tracker_538']
        else:
            if index == 0:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_capital_538 - row.Bet_538
            else:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_bets.loc[(index-1), 'Tracker_538'] - row.Bet_538
            
    return yesterdays_bets

##########RUN##########

# Run parameters
first_run = False
first_run_external = False
calculate_results = True
calculate_results_external = True

# Results calculation
if calculate_results:
    # Results calculation base
    if not first_run:
        results = pd.read_csv('results_tracker/results_tracker_base.csv', index_col = 0)
        results.reset_index(drop = True, inplace = True)
        yesterdays_capital = float(results.loc[len(results)-1, 'Money_Tracker'])
        yesterdays_bets = calculate_yesterdays_bets_results(yesterday_string = yesterday_string, yesterdays_capital = yesterdays_capital)
        results = results.append(yesterdays_bets)
        results.reset_index(drop = True, inplace = True)
        results.to_csv('results_tracker/results_tracker_base.csv')
        capital = float(results.loc[len(results)-1, 'Money_Tracker'])
    else:
        capital = 100000
else:
    try:
        results = pd.read_csv('results_tracker/results_tracker_base.csv', index_col = 0)
        capital = float(results.loc[len(results)-1, 'Money_Tracker'])
    except:
        capital = 100000
# Results calculation external
if calculate_results_external:
    if not first_run_external:
        yesterdays_capital_538 = 100000
        yesterdays_bets = calculate_yesterdays_bet_results_external(yesterday_string, yesterdays_capital_538)
        yesterdays_bets.reset_index(drop = True, inplace = True)
        yesterdays_bets.to_csv('results_tracker/results_tracker_external.csv')
        capital_538 = capital = float(yesterdays_bets.loc[len(yesterdays_bets)-1, 'Tracker_538'])

        # results = pd.read_csv('results_tracker/results_tracker_external.csv', index_col = 0)
        # yesterdays_capital_538 = float(results.loc[len(results)-1, 'Tracker_538'])
        # yesterdays_bets = calculate_yesterdays_bet_results_external(yesterday_string, yesterdays_capital_538)
        # results = results.append(yesterdays_bets)
        # results.reset_index(drop = True, inplace = True)
        # results.to_csv('results_tracker/results_tracker_external.csv')
        # capital_538 = capital = float(results.loc[len(results)-1, 'Tracker_538'])
    else:
        capital_538 = 100000
else:
    try:
        results = pd.read_csv('results_tracker/results_tracker_external.csv', index_col = 0)
        capital_538 = float(results.loc[len(results)-1, 'Tracker_538'])
    except:
        capital_538 = 100000

# Bets calculation

# Getting necessary inputs
frac_season = _calculate_frac_season()
active_rosters = retrieve_all_active_rosters(file_name = None)
todays_games = retrieve_todays_games_info()
retrieve_current_year_WAR()
current_year_WAR = load_current_year_WAR()
pt = load_combined_pecota_table()
odds = retrieve_odds()
# Calculating today's team win prob
current_run_differential = _calculate_cl_with_differential()
starting_rotations, failed_to_find_pitchers = retrieve_starting_rotations_WAR(pt, current_year_WAR)
print(failed_to_find_pitchers)
sp_adjustments = calculate_sp_adjustment(todays_games, starting_rotations, pt, frac_season = frac_season)
overall_war_predictions_preseason = pd.read_csv('data/overall_war_predictions_preseason.csv', index_col = 0)
active_roster_war, failed_to_find_players = calculate_active_roster_war_table(active_rosters, overall_war_predictions_preseason, current_year_WAR, pt, current_year, frac_season)
print(failed_to_find_players)
preseason_projections = pd.read_csv('data/preseason_projections.csv', index_col = 0)
todays_win_percentages = todays_win_percentages(preseason_projections, current_run_differential, sp_adjustments, active_roster_war, frac_season)
# Calculating today's bets
todays_bets = todays_bets(todays_games = todays_games, todays_win_percentages = todays_win_percentages, odds = odds, capital = capital, kelly = kelly)
todays_bets.drop_duplicates(inplace = True)
todays_bets.to_csv('past_bets/base/bets_' + today + '.csv')
print(sp_adjustments)

# Bets calculation_external

todays_bets_external = calculate_bets_external(capital_538)
todays_bets_external.to_csv('past_bets/external/bets_' + today + '.csv')