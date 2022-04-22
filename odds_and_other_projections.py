import pandas as pd
import datetime as dt
import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def _calculate_odds(odds):
    if odds<0:
        return (abs(odds)/(abs(odds)+100))*100
    if odds>0:
        return (100/(odds+100))*100

def retrieve_odds():
    
    # Team map
    team_map = {
    'CHC' : 'Cubs',
    'STL' : 'Cardinals',
    'MIN' : 'Twins',
    'DET' : 'Tigers',
    'BOS' : 'Red Sox',
    'TOR' : 'Blue Jays',
    'SEA' : 'Mariners',
    'HOU' : 'Astros',
    'SD' : 'Padres',
    'OAK' : 'Athletics',
    'BAL' : 'Orioles',
    'MIA' : 'Marlins',
    'PHI' : 'Phillies',
    'WSH' : 'Nationals',
    'NYM' : 'Mets',
    'ATL' : 'Braves',
    'TB' : 'Rays',
    'NYY' : 'Yankees',
    'TEX' : 'Rangers',
    'ARI' : 'Diamondbacks',
    'CHC' : 'Cubs',
    'CIN' : 'Reds',
    'KC' : 'Royals',
    'CWS' : 'White Sox',
    'LAA' : 'Angels',
    'COL' : 'Rockies',
    'SF' : 'Giants',
    'LAD' : 'Dodgers',
    'MIL' : 'Brewers',
    'PIT' : 'Pirates',
    'CLE' : 'Indians'
    }

    # Getting odds table and formatting
    tables = pd.read_html('https://www.actionnetwork.com/mlb/odds')
    odds = tables[0]
    odds = odds.iloc[::2]
    odds.reset_index(drop = True, inplace = True)

    # Iterating through to get home/away and odds
    odds_df = pd.DataFrame(columns = ['Home_Team', 'Away_Team', 'Home_Odds', 'Away_Odds'])
    for index, row in odds.iterrows():
        # Retreiving home and away teams
        teams = {}
        for key in team_map.keys():
            if row.Scheduled.find(key) != -1:
                teams[row.Scheduled.find(key)] = key
        keys = []
        for key in teams.keys():
            keys.append(key)
        if keys[0] > keys[1]:
            home_team = teams[keys[0]]
            away_team = teams[keys[1]]
        else:
            home_team = teams[keys[1]]
            away_team = teams[keys[0]]
        # Retreiving odds
        ml_string = row['Unnamed: 6']
        if len(ml_string) == 8:
            ml_away = ml_string[:4]
            ml_home = ml_string[-4:]
        if len(ml_string) == 9:
            if (ml_string[4] == '+') | (ml_string[4]=='-'):
                ml_away = ml_string[:4]
                ml_home = ml_string[-5:]
            else:
                ml_away = ml_string[:5]
                ml_home = ml_string[-4:]
        if len(ml_string) == 10:
                ml_away = ml_string[:5]
                ml_home = ml_string[-5:]
        try:
            ml_away = float(ml_away)
        except:
            continue
        try:
            ml_home = float(ml_home)
        except:
            continue
        series = pd.Series([home_team, away_team, ml_home, ml_away], index = odds_df.columns)
        odds_df = odds_df.append(series, ignore_index = True)
    odds_df['Home_Prob'] = odds_df.Home_Odds.apply(_calculate_odds)
    odds_df['Away_Prob'] = odds_df.Away_Odds.apply(_calculate_odds)
    odds_df['Home_Team'] = odds_df.Home_Team.apply(lambda x: team_map[x])
    odds_df['Away_Team'] = odds_df.Away_Team.apply(lambda x: team_map[x])
    return odds_df

def _retrieve_538():
    fivethirtyeight_team_mapping = {
    'MIAMarlins' : 'Marlins',
    'WSHNationals' : 'Nationals',
    'MILBrewers' : 'Brewers',
    'TORBlue Jays' : 'Blue Jays',
    'BALOrioles' : 'Orioles',
    'PHIPhillies' : 'Phillies',
    'PITPirates' : 'Pirates',
    'BOSRed Sox' : 'Red Sox',
    'STLCardinals' : 'Cardinals',
    'CLEIndians' : 'Indians',
    'ATLBraves' : 'Braves',
    'NYMMets' : 'Mets',
    'NYYYankees' : 'Yankees',
    'TBRays' : 'Rays',
    'CINReds' : 'Reds',
    'CHCCubs' : 'Cubs',
    'ARIDiamondbacks' : 'Diamondbacks',
    'TEXRangers' : 'Rangers',
    'CHWWhite Sox' : 'White Sox',
    'KCRoyals' : 'Royals',
    'DETTigers' : 'Tigers',
    'MINTwins' : 'Twins',
    'COLRockies' : 'Rockies',
    'LAAAngels' : 'Angels',
    'LADDodgers' : 'Dodgers',
    'SFGiants' : 'Giants',
    'OAKAthletics' : 'Athletics',
    'SDPadres' : 'Padres',
    'HOUAstros' : 'Astros',
    'SEAMariners' : 'Mariners'
    }
    regex = r'\d+/\d+'
    tables = pd.read_html('https://projects.fivethirtyeight.com/2021-mlb-predictions/games/')
    fivethirtyeight = tables[0][['Date', 'Team', 'Win prob.Chance of winning']]
    fivethirtyeight.columns = ['Date', 'Team', 'Win Probability']
    fivethirtyeight.head()
    evens = fivethirtyeight.iloc[::2]
    evens.reset_index(drop = True, inplace = True)
    odds = fivethirtyeight.iloc[1::2]
    odds.reset_index(drop = True, inplace = True)
    final_538 = pd.merge(evens, odds, left_on = evens.index, right_on = odds.index)
    final_538.drop(['key_0', 'Date_y'], axis = 1, inplace = True)
    final_538.columns = ['Date', 'Away_Team', 'Away_Prob', 'Home_Team', 'Home_Prob']
    final_538['Away_Team'] = final_538['Away_Team'].apply(lambda x: fivethirtyeight_team_mapping[x])
    final_538['Home_Team'] = final_538['Home_Team'].apply(lambda x: fivethirtyeight_team_mapping[x])
    final_538['Date'] = final_538.Date.apply(lambda x: re.findall(regex,x))
    final_538['Date'] = final_538.Date.apply(lambda x: x[0])
    final_538['Date'] = pd.to_datetime(final_538.Date, format = '%m/%d')
    return final_538

def _retrieve_athletic():
    athletic_team_mapping = {
    'MIL' : 'Brewers',
    'PIT' : 'Pirates',
    'WAS' : 'Nationals',
    'PHI' : 'Phillies',
    'MIA' : 'Marlins',
    'BAL' : 'Orioles',
    'STL' : 'Cardinals',
    'CLE' : 'Indians',
    'ATL' : 'Braves',
    'NYM' : 'Mets',
    'TOR' : 'Blue Jays',
    'BOS' : 'Red Sox',
    'NYY' : 'Yankees',
    'TBR' : 'Rays',
    'CIN' : 'Reds',
    'CHC' : 'Cubs',
    'ARI' : 'Diamondbacks',
    'TEX' : 'Rangers',
    'CHW' : 'White Sox',
    'KCR' : 'Royals',
    'DET' : 'Tigers',
    'MIN' : 'Twins',
    'COL' : 'Rockies',
    'LAA' : 'Angels',
    'LAD' : 'Dodgers',
    'SFG' : 'Giants',
    'HOU' : 'Astros',
    'SEA' : 'Mariners',
    'OAK' : 'Athletics',
    'SDP' : 'Padres'
    }

    url = 'https://theathletic.com/2730730/2021/07/26/baseball-daily-picks-from-mlb-model-odds-expected-value-and-more-from-the-bat-x-for-mondays-games-2/'
    options = Options()
    options.add_argument("user-data-dir=/Users/hsinger24/Library/Application Support/Google/Chrome/Default1")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    log_in = browser.find_element_by_xpath("//*[@id='navbar-top']/div/div/div/div[3]/div/a[1]")
    log_in.click()
    time.sleep(0.25)
    log_in_email = browser.find_element_by_xpath("//*[@id='email-login-button']")
    log_in_email.click()
    time.sleep(0.25)
    email = browser.find_element_by_xpath("//*[@id='email-login-form']/div[2]/input")
    email.click()
    time.sleep(0.25)
    email.send_keys('singerfam1@gmail.com')
    password = browser.find_element_by_xpath("//*[@id='email-login-form']/div[3]/input")
    password.click()
    time.sleep(0.25)
    password.send_keys('Tredwell01!')
    log_in = browser.find_element_by_xpath("//*[@id='email-login-form']/button")
    log_in.click()
    time.sleep(0.5)
    html = browser.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    tables = pd.read_html(html)
    athletic_table = tables[0]
    athletic_table.dropna(inplace = True)
    athletic_table.reset_index(drop = True, inplace = True)
    athletic_table['Home_Team'] = athletic_table['GAME'].str.split(' ')
    athletic_table['Home_Team'] = athletic_table['Home_Team'].apply(lambda x: x[0])
    athletic_table['Away_Team'] = athletic_table['GAME'].str.split(' ')
    athletic_table['Away_Team'] = athletic_table['Away_Team'].apply(lambda x: x[2])
    athletic_table['Home_Team'] = athletic_table['Home_Team'].apply(lambda x: athletic_team_mapping[x])
    athletic_table['Away_Team'] = athletic_table['Away_Team'].apply(lambda x: athletic_team_mapping[x])
    athletic_table.drop(['TIME', 'GAME'], inplace = True, axis = 1)
    evens = athletic_table.iloc[::2]
    evens.reset_index(drop = True, inplace = True)
    odds = athletic_table.iloc[1::2]
    odds.reset_index(drop = True, inplace = True)
    final_athletic = pd.merge(evens, odds, left_on = evens.index, right_on = odds.index)
    final_athletic = final_athletic[['DATE_x','Home_Team_x', 'Away_Team_x', 'THE BAT XWIN%_x', 'THE BAT XWIN%_y']]
    final_athletic.columns = ['Date','Away_Team', 'Home_Team', 'Away_Prob', 'Home_Prob']
    browser.quit()
    final_athletic['Date'] = pd.to_datetime(final_athletic.Date, format = "%m/%d")
    return final_athletic

def retrieve_external_data(file_path = 'data/external_data.csv'):
    """Retrieves and merges the models from 538, The Athletic, and today's odds
    Args:
        file_path (str, optional): path to save file. Defaults to "data/external_data.csv".
    Returns:
        pandas.DataFrame: The merged external data table
    """

    merged = pd.merge(_retrieve_athletic(), _retrieve_538(), on = ['Home_Team', 'Away_Team', 'Date'], how = 'inner')
    merged.columns = ['Date', 'Away_Team', 'Home_Team','Away_Prob_Athletic', 'Home_Prob_Athletic', 'Away_Prob_538', 
                    'Home_Prob_538']
    final = pd.merge(retrieve_odds(), merged, on = ['Home_Team', 'Away_Team'], how = 'inner')
    final.drop(['Home_Odds', 'Away_Odds'], axis = 1, inplace = True)
    final = final[['Date', 'Away_Team', 'Home_Team','Away_Prob_Athletic', 'Home_Prob_Athletic',
                'Away_Prob_538', 'Home_Prob_538', 'Away_Prob', 'Home_Prob']]
    final.columns = ['Date', 'Away_Team', 'Home_Team','Away_Prob_Athletic', 'Home_Prob_Athletic', 'Away_Prob_538', 
                    'Home_Prob_538', 'Away_Prob_Implied', 'Home_Prob_Implied']
    final['Date'] = dt.date.today()
    final.dropna(inplace = True)
    odds = retrieve_odds()
    merged = pd.merge(final, odds, on = ['Home_Team', 'Away_Team'], how = 'inner')
    merged = merged[['Date', 'Away_Team', 'Home_Team', 'Away_Prob_Athletic', 'Home_Prob_Athletic', 'Away_Prob_538', 
    'Home_Prob_538', 'Home_Odds', 'Away_Odds', 'Home_Prob', 'Away_Prob']]
    merged.columns = ['Date', 'Away_Team', 'Home_Team','Away_Prob_Athletic', 'Home_Prob_Athletic', 'Away_Prob_538', 
                        'Home_Prob_538', 'Home_ML', 'Away_ML', 'Home_Prob_Implied', 'Away_Prob_Implied']
    merged['Away_Prob_Athletic'] = merged.Away_Prob_Athletic.str.strip('%')
    merged['Away_Prob_Athletic'] = merged.Away_Prob_Athletic.astype(float)
    merged['Away_Prob_Athletic'] = merged.Away_Prob_Athletic/100
    merged['Home_Prob_Athletic'] = merged.Home_Prob_Athletic.str.strip('%')
    merged['Home_Prob_Athletic'] = merged.Home_Prob_Athletic.astype(float)
    merged['Home_Prob_Athletic'] = merged.Home_Prob_Athletic/100
    merged['Away_Prob_538'] = merged.Away_Prob_538.str.strip('%')
    merged['Away_Prob_538'] = merged.Away_Prob_538.astype(float)
    merged['Away_Prob_538'] = merged.Away_Prob_538/100
    merged['Home_Prob_538'] = merged.Home_Prob_538.str.strip('%')
    merged['Home_Prob_538'] = merged.Home_Prob_538.astype(float)
    merged['Home_Prob_538'] = merged.Home_Prob_538/100
    merged['Away_Prob_Implied'] = merged.Away_Prob_Implied/100
    merged['Home_Prob_Implied'] = merged.Home_Prob_Implied/100
    if file_path is not None:
        with open(file_path, "w") as f:
            merged.to_csv(f)

    return merged

def load_external_data(file_path = 'data/external_data.csv'):
    """Loads external data table from a given file
    Args:
        file_path (str, optional): War file. Defaults to "data/external_data.csv".
    Returns:
        pandas.DataFrame: External Data Table
    """
    return pd.read_csv(file_path, index_col=0)
