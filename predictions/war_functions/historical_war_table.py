from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import re

team_map = {
    'LAD': 'Dodgers',
    'SD': 'Padres',
    'CWS': 'White Sox',
    'MIN': 'Twins',
    'CLE': 'Indians',
    'OAK': 'Athletics',
    'TB': 'Rays',
    'NYY': 'Yankees',
    'ATL': 'Braves',
    'NYM': 'Mets',
    'CHC': 'Cubs',
    'CIN': 'Reds',
    'LAA': 'Angels',
    'MIL': 'Brewers',
    'SF': 'Giants',
    'PHI': 'Phillies',
    'HOU': 'Astros',
    'STL': 'Cardinals',
    'KC': 'Royals',
    'BAL': 'Orioles',
    'SEA': 'Mariners',
    'TOR': 'Blue Jays',
    'DET': 'Tigers',
    'BOS': 'Red Sox',
    'ARI': 'Diamondbacks',
    'WSH': 'Nationals',
    'COL': 'Rockies',
    'MIA': 'Marlins',
    'PIT': 'Pirates',
    'TEX': 'Rangers'
}

def _retrieve_offense_war_table_failed(year):
    # year = str(year)
    # offense_war_html = pd.read_html(
    #     f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season={year}&month=0&season1={year}&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=&enddate=')

    # TEAM_WAR_TABLE_INDEX = 16

    # # Find the correct table
    # offense_war_table = offense_war_html[TEAM_WAR_TABLE_INDEX]

    # # Set up dataframe by adjusting columns
    # offense_war_table_columns = []
    # for _, j in offense_war_table.columns:
    #     offense_war_table_columns.append(j)
    # offense_war_table.columns = offense_war_table_columns
    # offense_war_table_final = offense_war_table.loc[:, ['Team', 'WAR']]

    # return offense_war_table_final
    return None

def _retrieve_defense_war_table_failed(year):
    # """Retrieves the Defensive WAR table. Should not be used outside this file

    # Args:
    #     year (int): the year to retrieve the war table for

    # Returns:
    #     pandas.DataFrame: The War table
    # """
    # year = str(year)
    # TEAM_WAR_TABLE_INDEX = 16
    # defense_war_html = pd.read_html(
    #     f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season={year}&month=0&season1={year}&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=&enddate=')

    # # get the correct table
    # defense_war_table = defense_war_html[TEAM_WAR_TABLE_INDEX]

    # # set up dataframe by adjusting columns
    # defense_war_table_columns = []
    # for _, j in defense_war_table.columns:
    #     defense_war_table_columns.append(j)
    # defense_war_table.columns = defense_war_table_columns
    # defense_war_table_final = defense_war_table.loc[:, ['Team', 'WAR']]

    return None

def retrieve_historical_combined_war_table_failed(year, file_path="data/war_table.csv"):
    # """Retrieves the Offensive and Defensive War tables for a given year (past) and saves it to a file,
    # if the given file_path is not None

    # Args:
    #     year (int): Year to get
    #     file_path (str, optional): path to save file. Defaults to "data/war_table.csv".

    # Returns:
    #     pandas.DataFrame: The War table
    # """
    # # get both offense and defense tables
    # offense_table = _retrieve_offense_war_table(year)
    # defense_table = _retrieve_defense_war_table(year)

    # # merge tables
    # war = pd.merge(offense_table, defense_table, on='Team')

    # # adjust columns and create a total war column
    # war.columns = ['Team', 'Offense', 'Defense']
    # war.drop(30, inplace=True)
    # war.Offense = pd.to_numeric(war['Offense'])
    # war.Defense = pd.to_numeric(war.Defense)
    # war['Total'] = war.Offense + war.Defense
    # war.sort_values(by='Total', ascending=False, inplace=True)
    # war.Team = war.Team.apply(lambda x: team_map[x])

    # if file_path is not None:
    #     with open(file_path, "w") as f:
    #         war.to_csv(f)

    return None

def retrieve_previous_year_war_table(previous_year, file_path="data/historical_war_table.csv"):
    """Retrieves previous year war table and saves it to a file,
    if the given file_path is not None

    Args:
        previous year
        file_path (str, optional): path to save file. Defaults to "data/war_table.csv".

    Returns:
        pandas.DataFrame: The previous year's WAR table by team
    """
    
    driver = webdriver.Chrome('../chromedriver')
    driver.get('https://www.baseballprospectus.com/leaderboards/hitting/')
    regex_name = r'(\D+\s\D+)+'
    table_dict = {}
    filters = driver.find_elements_by_class_name('filter-btn')
    year_filter = filters[0]
    year_filter.click()
    time.sleep(1)
    year_input = driver.find_element_by_name('currentSliderValue')
    year_input.clear()
    year_input.send_keys(str(previous_year))
    save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div[2]/button[2]")
    save_button.click()
    time.sleep(3)
    for i in range(30):
        if i==0:
            filters = driver.find_elements_by_class_name('filter-btn')
            team_filter = filters[3] # this is the team filter
            team_filter.click() # this is the team filter
            team_options = driver.find_elements_by_class_name('multi-select__box') # Finds all the teams buttons
            team_options[i].click() # deselects the all button so you can select a single team
            team_options[(i+1)].click() # Clicks Baltimore
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[4]/div/div/div/div[2]/button[2]")
            save_button.click() # clicks save button
            plate_appearance_filter = filters[4]
            plate_appearance_filter.click() # Clicking plate appearance filter
            time.sleep(5)
            plate_appearance_input = driver.find_element_by_name('currentSliderValue')
            plate_appearance_input.clear()
            plate_appearance_input.send_keys('0')
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[5]/div/div/div/div[2]/button[2]")
            save_button.click()
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            html = driver.page_source
            hitting_table = pd.read_html(html)
            hitting_table = hitting_table[0]
            hitting_table = hitting_table.iloc[0:(hitting_table.shape[0]), [0,2,3]]
            hitting_table.columns = ['Name', 'Team', 'WAR']
            hitting_table['Name'] = hitting_table.Name.apply(lambda x: re.findall(regex_name, x)[0])
            hitting_table['Name'] = hitting_table.Name.apply(lambda x: x.strip(' '))
            team_name = hitting_table.iloc[0,1]
            table_dict[team_name] = pd.DataFrame(columns = hitting_table.columns)
            table_dict[team_name] = table_dict[team_name].append(hitting_table)
            print(team_name)
        else:
            time.sleep(5)
            team_filter.click()
            time.sleep(5)
            team_options = driver.find_elements_by_class_name('multi-select__box')
            team_options[i].click()
            team_options[(i+1)].click()
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[4]/div/div/div/div[2]/button[2]")
            save_button.click()
            time.sleep(5)
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            html = driver.page_source
            hitting_table = pd.read_html(html)
            hitting_table = hitting_table[0]
            hitting_table = hitting_table.iloc[0:(hitting_table.shape[0]), [0,2,3]]
            hitting_table.columns = ['Name', 'Team', 'WAR']
            hitting_table['Name'] = hitting_table.Name.apply(lambda x: re.findall(regex_name, x)[0])
            hitting_table['Name'] = hitting_table.Name.apply(lambda x: x.strip(' '))
            team_name = hitting_table.iloc[0,1]
            table_dict[team_name] = pd.DataFrame(columns = hitting_table.columns)
            table_dict[team_name] = table_dict[team_name].append(hitting_table)
            print(team_name)
    # Getting pitchers
    driver.get('https://www.baseballprospectus.com/leaderboards/pitching/')
    filters = driver.find_elements_by_class_name('filter-btn')
    year_filter = filters[0]
    year_filter.click()
    time.sleep(1)
    year_input = driver.find_element_by_name('currentSliderValue')
    year_input.clear()
    year_input.send_keys(str(previous_year))
    save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div[2]/button[2]")
    save_button.click()
    time.sleep(3)
    for i in range(30):
        if i==0:
            time.sleep(5)
            filters = driver.find_elements_by_class_name('filter-btn')
            team_filter = filters[3]
            team_filter.click()
            team_options = driver.find_elements_by_class_name('multi-select__box')
            team_options[i].click()
            team_options[(i+1)].click()
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[4]/div/div/div/div[2]/button[2]")
            save_button.click()
            innings_filter = filters[4]
            innings_filter.click()
            time.sleep(5)
            innings_input = driver.find_element_by_name('currentSliderValue')
            innings_input.clear()
            innings_input.send_keys('0')
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[5]/div/div/div/div[2]/button[2]")
            save_button.click()
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            html = driver.page_source
            pitching_table = pd.read_html(html)
            pitching_table = pitching_table[0]
            pitching_table = pitching_table.iloc[0:(pitching_table.shape[0]), [0,2,3]]
            pitching_table.columns = ['Name', 'Team', 'WAR']
            pitching_table['Name'] = pitching_table.Name.apply(lambda x: re.findall(regex_name, x)[0])
            pitching_table['Name'] = pitching_table.Name.apply(lambda x: x.strip(' '))
            team_name = pitching_table.iloc[0,1]
            table_dict[team_name] = table_dict[team_name].append(pitching_table)
            print(team_name)
        else:
            time.sleep(5)
            team_filter.click()
            time.sleep(5)
            team_options = driver.find_elements_by_class_name('multi-select__box')
            team_options[i].click()
            team_options[(i+1)].click()
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[4]/div/div/div/div[2]/button[2]")
            save_button.click()
            time.sleep(5)
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
                load_button = driver.find_element_by_class_name('load-more__btn')
                load_button.click()
            except:
                pass
            html = driver.page_source
            pitching_table = pd.read_html(html)
            pitching_table = pitching_table[0]
            pitching_table = pitching_table.iloc[0:(pitching_table.shape[0]), [0,2,3]]
            pitching_table.columns = ['Name', 'Team', 'WAR']
            pitching_table['Name'] = pitching_table.Name.apply(lambda x: re.findall(regex_name, x)[0])
            pitching_table['Name'] = pitching_table.Name.apply(lambda x: x.strip(' '))
            team_name = pitching_table.iloc[0,1]
            table_dict[team_name] = table_dict[team_name].append(pitching_table)
            print(team_name)
    big_boi_df = pd.DataFrame()
    for key, value in table_dict.items():
        big_boi_df = big_boi_df.append(value)
    def conv(x):
        try:
            return float(x)
        except:
            return 0
    big_boi_df['WAR'] = big_boi_df['WAR'].apply(conv)
    grouped = big_boi_df.groupby(by = 'Team')['WAR'].sum()
    grouped = pd.DataFrame(grouped)
    grouped.reset_index(inplace = True)
    grouped.columns = ['Team', 'WAR']
    grouped['Team'] = grouped.Team.apply(lambda x: team_map[x])
    grouped.drop('Unnamed: 0', axis = 1, inplace = True)

    if file_path is not None:
        with open(file_path, "w") as f:
            grouped.to_csv(f)

    return grouped

def load_previous_year_war_table(file_path="data/historical_war_table.csv"):
    """Loads historical war table from a given file

    Args:
        file_path (str, optional): War file. Defaults to "data/historical_war_table.csv".

    Returns:
        pandas.DataFrame: War Table
    """
    return pd.read_csv(file_path, index_col=0)




