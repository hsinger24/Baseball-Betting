########## IMPORTS AND NECESSARY PARAMETERS ##########
import pandas as pd
import datetime as dt
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
today = dt.date.today()
yesterday = today - dt.timedelta(days=1)
yesterday_string = str(yesterday)
yesterday_string = yesterday_string.replace('-', '')
yesterdays_capital = float(input("Hank, please input yesterday's capital for the base model: "))
yesterdays_capital_athletic = float(input("Hank, please input yesterday's capital for the Athletic model: "))
yesterdays_capital_538 = float(input("Hank, please input yesterday's capital for the 538 model: "))
yesterdays_capital_combined = float(input("Hank, please input yesterday's capital for the combined model: "))

########## RUN DAILY TO CALCULATE YESTERDAYS RESULTS AND UPDATE TRACKER FOR BASE MODEL ##########

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
        if (row.Home_Team not in results_table['Winner'].values) & (row.Away_Team not in results_table['Winner'].values):
            yesterdays_bets.loc[index, 'Home_Bet'] = 0
            yesterdays_bets.loc[index, 'Away_Bet'] = 0
            payoff = 0
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

yesterdays_bets = calculate_yesterdays_bets_results(yesterday_string = yesterday_string, yesterdays_capital = yesterdays_capital)
results_tracker_base = pd.read_csv('results_tracker/results_tracker_base.csv')
results_tracker_base = results_tracker_base.append(yesterdays_bets)
results_tracker_base.to_csv('results_tracker/results_tracker_base.csv')

########## RUN DAILY TO CALCULATE YESTERDAYS RESULTS AND UPDATE TRACKER FOR EXTERNAL MODELS ##########

def calculate_payoff_external(row, Athletic = False, Fivethirtyeight = False, Combined = False):
    if Athletic:
        if row.Bet_Athletic<=0:
            payoff = 0
        else:
            if row.Home_KC_Athletic>0:
                if row.Home_ML>0:
                    payoff = (row.Home_ML/100)*row.Bet_Athletic
                if row.Home_ML<0:
                    payoff = row.Bet_Athletic/((abs(row.Home_ML)/100))
            if row.Away_KC_Athletic>0:
                if row.Away_ML>0:
                    payoff = (row.Away_ML/100)*row.Bet_Athletic
                if row.Away_ML<0:
                    payoff = row.Bet_Athletic/((abs(row.Away_ML)/100))
    if Fivethirtyeight:
        if row.Bet_538<=0:
            payoff = 0
        else:
            if row.Home_KC_538>0:
                if row.Home_ML>0:
                    payoff = (row.Home_ML/100)*row.Bet_538
                if row.Home_ML<0:
                    payoff = row.Bet_538/((abs(row.Home_ML)/100))
            if row.Away_KC_538>0:
                if row.Away_ML>0:
                    payoff = (row.Away_ML/100)*row.Bet_538
                if row.Away_ML<0:
                    payoff = row.Bet_538/((abs(row.Away_ML)/100))
    if Combined:
        if row.Bet_Combined<=0:
            payoff = 0
        else:
            if row.Home_Combined>0:
                if row.Home_ML>0:
                    payoff = (row.Home_ML/100)*row.Bet_Combined
                if row.Home_ML<0:
                    payoff = row.Bet_Combined/((abs(row.Home_ML)/100))
            if row.Away_Combined>0:
                if row.Away_ML>0:
                    payoff = (row.Away_ML/100)*row.Bet_Combined
                if row.Away_ML<0:
                    payoff = row.Bet_Combined/((abs(row.Away_ML)/100))
    return payoff

def calculate_yesterdays_bets_results_external(yesterday_string, yesterdays_capital_athletic, yesterdays_capital_538, yesterdays_capital_combined): 
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
    yesterdays_bets = pd.read_csv('past_bets/external/bets_external_' + yesterday_string + '.csv', index_col = 0)
    yesterdays_bets['Home_Team'] = yesterdays_bets['Home_Team'].apply(lambda x: team_map[x])
    yesterdays_bets['Away_Team'] = yesterdays_bets['Away_Team'].apply(lambda x: team_map[x])
    yesterdays_bets = yesterdays_bets[(yesterdays_bets.Bet_Athletic>0) | (yesterdays_bets.Bet_538>0) | (yesterdays_bets.Bet_Combined>0)]
    yesterdays_bets.reset_index(drop = True, inplace = True)
    yesterdays_bets['Won_Athletic'] = 0
    yesterdays_bets['Tracker_Athletic'] = 0
    yesterdays_bets['Won_538'] = 0
    yesterdays_bets['Tracker_538'] = 0
    yesterdays_bets['Won_Combined'] = 0
    yesterdays_bets['Tracker_Combined'] = 0
    for index, row in yesterdays_bets.iterrows():
        home_team = row.Home_Team
        away_team = row.Away_Team
        payoff_athletic = calculate_payoff_external(row, Athletic = True)
        payoff_538 = calculate_payoff_external(row, Fivethirtyeight = True)
        payoff_combined = calculate_payoff_external(row, Combined = True)
        if (home_team not in results_table['Winner'].values) & (away_team not in results_table['Winner'].values):
            yesterdays_bets.loc[index, 'Won_Athletic'] = -1
            yesterdays_bets.loc[index, 'Won_538'] = -1
            yesterdays_bets.loc[index, 'Won_Combined'] = -1
        if row.Bet_Athletic>0:
            if (row.Home_KC_Athletic>0) & (home_team in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_Athletic'] = 1
            elif (row.Away_KC_Athletic>0) & (away_team in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_Athletic'] = 1
            else:
                yesterdays_bets.loc[index, 'Won_Athletic'] = 0
        else:
            yesterdays_bets.loc[index, 'Won_Athletic'] = -1
        if row.Bet_538>0:
            if (row.Home_KC_538>0) & (home_team in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_538'] = 1
            elif (row.Away_KC_538>0) & (away_team in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_538'] = 1
            else:
                yesterdays_bets.loc[index, 'Won_538'] = 0
        else:
            yesterdays_bets.loc[index, 'Won_538'] = -1
        if row.Bet_Combined>0:
            if (row.Home_Combined>0) & (home_team in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_Combined'] = 1
            elif (row.Away_Combined>0) & (away_team in results_table['Winner'].values):
                yesterdays_bets.loc[index, 'Won_Combined'] = 1
            else:
                yesterdays_bets.loc[index, 'Won_Combined'] = 0
        else:
            yesterdays_bets.loc[index, 'Won_Combined'] = -1
        if yesterdays_bets.loc[index, 'Won_Athletic'] == 1:
            if index == 0:
                yesterdays_bets.loc[index, 'Tracker_Athletic'] = yesterdays_capital_athletic + payoff_athletic
            else:
                yesterdays_bets.loc[index, 'Tracker_Athletic'] = yesterdays_bets.loc[(index-1), 'Tracker_Athletic'] + payoff_athletic
        else:
            if index == 0:
                yesterdays_bets.loc[index, 'Tracker_Athletic'] = yesterdays_capital_athletic - row.Bet_Athletic
            else:
                yesterdays_bets.loc[index, 'Tracker_Athletic'] = yesterdays_bets.loc[(index-1), 'Tracker_Athletic'] - row.Bet_Athletic
        if yesterdays_bets.loc[index, 'Won_538'] == 1:
            if index == 0:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_capital_538 + payoff_538
            else:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_bets.loc[(index-1), 'Tracker_538'] + payoff_538
        else:
            if index == 0:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_capital_538 - row.Bet_538
            else:
                yesterdays_bets.loc[index, 'Tracker_538'] = yesterdays_bets.loc[(index-1), 'Tracker_538'] - row.Bet_538
        if yesterdays_bets.loc[index, 'Won_Combined'] == 1:
            if index == 0:
                yesterdays_bets.loc[index, 'Tracker_Combined'] = yesterdays_capital_combined + payoff_combined
            else:
                yesterdays_bets.loc[index, 'Tracker_Combined'] = yesterdays_bets.loc[(index-1), 'Tracker_Combined'] + payoff_combined
        else:
            if index == 0:
                yesterdays_bets.loc[index, 'Tracker_Combined'] = yesterdays_capital_combined - row.Bet_Combined
            else:
                yesterdays_bets.loc[index, 'Tracker_Combined'] = yesterdays_bets.loc[(index-1), 'Tracker_Combined'] - row.Bet_Combined
         
    return yesterdays_bets

yesterdays_bets = calculate_yesterdays_bets_results_external(yesterday_string = yesterday_string, 
    yesterdays_capital_athletic = yesterdays_capital_athletic, yesterdays_capital_538 = yesterdays_capital_538,
    yesterdays_capital_combined =  yesterdays_capital_combined)
results_tracker_external = pd.read_csv('results_tracker/results_tracker_external.csv')
results_tracker_external = results_tracker_external.append(yesterdays_bets)
results_tracker_external.to_csv('results_tracker/results_tracker_external.csv')