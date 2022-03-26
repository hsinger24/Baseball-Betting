from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import re
import json
import unidecode

team_map = {
    'LAD': 'Dodgers',
    'SD': 'Padres',
    'CWS': 'White Sox',
    'CHW': 'White Sox',
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
    'WAS': 'Nationals',
    'COL': 'Rockies',
    'MIA': 'Marlins',
    'PIT': 'Pirates',
    'TEX': 'Rangers'
}

def _get_driver_location():
    with open("driver.json", 'r') as f:
        dct = json.load(f)
    
    return dct

def _retrieve_historical_player_war_tables(driver, year=None):
    # create dict to store team's player tables
    table_dict = {}
    regex_name = r'(\D+\s\D+)+'

    for j in range(2):
        if j == 1:
            driver.get("https://www.baseballprospectus.com/leaderboards/hitting/")
        else:
            driver.get("https://www.baseballprospectus.com/leaderboards/pitching/")
    
        # list of filters
        filters = driver.find_elements_by_class_name("filter-btn")

        # get the current year
        year_filter = filters[0]
        year_current = year_filter.text[-4:]

        # if the current year is the year given then do nothing
        # otherwise change the year filter
        if year is not None and (str(year) != year_current):

            # set the year to the given year
            year_filter.click()
            year_slider = driver.find_element_by_name("currentSliderValue")
            year_slider.clear()
            year_slider.send_keys(year)

            # get the save button, click it and wait for it to be stale
            save_btn = driver.find_elements_by_class_name("modal__btn--save")[0]
            save_btn.click()
            WebDriverWait(driver, 30).until(EC.staleness_of(save_btn))

        # Set PA/IP to 0    
        plate_apearance_innings_pitched_filter = filters[4]
        plate_apearance_innings_pitched_filter.click()
        pa_slider = driver.find_element_by_name("currentSliderValue")
        pa_slider.clear()
        pa_slider.send_keys(0)

        # save selection
        save_btn = driver.find_elements_by_class_name("modal__btn--save")[0]
        save_btn.click()
        WebDriverWait(driver, 30).until(EC.staleness_of(save_btn))

        # unclick the default all selection
        team_filter = filters[3]
        team_filter.click()
        teams = driver.find_elements_by_class_name("multi-select__box")
        all_btn = teams[0]
        all_btn.click()

        def to_num(x):
            try: return float(x)
            except: return 0.0

        # For every team
        for i in range(1, 31):
            # click the correct team
            team_btn = driver.find_elements_by_class_name("multi-select__box")[i]
            team_btn.click()

            # click save
            save_btn = driver.find_elements_by_class_name("modal__btn--save")
            save_btn = save_btn[0]
            save_btn.click()

            # wait for save button staleness
            WebDriverWait(driver, 30).until(
                EC.staleness_of(save_btn)
            )

            # click load till you can't click no mo

            # get the load button
            load_more_button = driver.find_elements_by_class_name("load-more__btn")[0]
            # click load while it is not disabled, but if it's inactive then also don't click it
            while len(driver.find_elements_by_class_name("load-more__btn--disabled")) == 0:
                if len(driver.find_elements_by_class_name("load-more__btn--inactive")) > 0:
                    continue
                load_more_button.click()

            # download team....
            
            html = driver.page_source
            player_table = pd.read_html(html)
            player_table = player_table[0]
            
            player_table = player_table.iloc[:, [0,2,3,9,6,8]]
            player_table.columns = ['Name', 'Team', 'WAR', 'GS_P', 'GS_H', 'Games_P']

            if j==0:
                player_table['Position'] = 'P'
                player_table['GS_H'] = 0
            else:
                player_table['Position'] = 'H'
                player_table['GS_P'] = 0
                player_table['Games_P'] = 0
           
            player_table['Name'] = player_table.Name.apply(lambda x: re.findall(regex_name, x)[0])
            player_table['Name'] = player_table.Name.apply(lambda x: x.strip(' '))

            player_table['WAR'] = player_table.WAR.apply(to_num)

            team_name = player_table.iloc[0,1]
            if j == 1:
                table_dict[team_name] = table_dict[team_name].append(player_table)
            else:
                table_dict[team_name] = pd.DataFrame(columns = player_table.columns)
                table_dict[team_name] = player_table

            # print(team_name)

            # Unclick the team
            team_filter.click()
            team_btn = driver.find_elements_by_class_name("multi-select__box")[i]
            team_btn.click()
        
        
    return table_dict

def retrieve_current_year_WAR(file_path = "data/curr_war_table.csv"):
    """Retrieves the current year WAR of all players who have played in the MLB this season from 
    baseball prospectus

    Args:
        file_path (str, optional): path to save file. Defaults to "data/curr_war_table.csv".

    Returns:
        pandas.DataFrame: The current year war table
    """
    # driver_dict = _get_driver_location()
    # driver = None
    # if driver_dict['driver_type'] == 'Chrome':
    #     driver = webdriver.Chrome(driver_dict['driver_loc'])
    # elif driver_dict['driver_type'] == 'Firefox':
    #     driver = webdriver.Firefox(driver_dict['driver_loc'])
    # else:
    #     print("Error")
    #     return
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Creates big df with all players, grouped by Name to get total WAR for each player
    table_dict = _retrieve_historical_player_war_tables(driver)
    driver.quit()
    all_players = pd.DataFrame()
    for key, value in table_dict.items():
        all_players = all_players.append(value)
    #grouped = all_players.groupby(by = 'Name')['WAR'].sum()
    grouped = all_players.groupby(by = 'Name').agg({'WAR' : 'sum', 'GS_P' : 'sum', 'GS_H' : 'sum', 'Games_P' : 'sum'})
    grouped = pd.DataFrame(grouped)
    grouped.reset_index(inplace = True)
    #grouped.columns = ['Name', 'WAR']
    grouped.columns = ['Name', 'WAR', 'GS_P', 'GS_H', 'Games_P']
    grouped['Name'] = grouped.Name.apply(unidecode.unidecode)

    # Adding GS and position
    drop_duplicated = all_players.drop_duplicates(subset = 'Name', keep = 'first')
    #drop_duplicated = drop_duplicated[['Name', 'GS_P', 'GS_H', 'Games_P', 'Position']]
    drop_duplicated = drop_duplicated[['Name', 'Position']]
    drop_duplicated['Name'] = drop_duplicated.Name.apply(unidecode.unidecode)
    final = pd.merge(grouped, drop_duplicated, on = 'Name', how = 'inner')
    final = final.drop_duplicates(subset = 'Name', keep = 'first')

    # Saving data to specified location
    if file_path is not None:
        with open("data/curr_war_table.csv", 'w') as f:
            final.to_csv(f)

    return final

def load_current_year_WAR(file_path = "data/curr_war_table.csv"):
    """Loads the current year war Table from a given file

    Args:
        file_path (str, optional): War file. Defaults to "data/curr_war_table.csv".

    Returns:
        pandas.DataFrame: Current year War Table
    """

    return pd.read_csv(file_path, index_col = 0)

def retrieve_previous_year_war_table(previous_year, file_path="data/historical_war_table.csv"):
    """Retrieves the previous year WAR for all players from Baseball Prospectus

    Args:
        - previous_year: year of interest
        - file_path (str, optional): path to save file. Defaults to "data/historical_war_table.csv".

    Returns:
        pandas.DataFrame: The current year war table
    """
    # driver_dict = _get_driver_location()
    # driver = None
    # if driver_dict['driver_type'] == 'Chrome':
    #     driver = webdriver.Chrome(driver_dict['driver_loc'])
    # elif driver_dict['driver_type'] == 'Firefox':
    #     driver = webdriver.Firefox(driver_dict['driver_loc'])
    # else:
    #     print("Error")
    #     return
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Returns WAR for each team from the previous year
    table_dict = _retrieve_historical_player_war_tables(driver, year = previous_year)
    driver.quit()
    big_boi_df = pd.DataFrame()
    for key, value in table_dict.items():
        big_boi_df = big_boi_df.append(value)
    grouped = big_boi_df.groupby(by = 'Team')['WAR'].sum()
    grouped = pd.DataFrame(grouped)
    grouped.reset_index(inplace = True)
    grouped.columns = ['Team', 'WAR']
    grouped['Team'] = grouped.Team.apply(lambda x: team_map[x])

    # Saves file to specified location
    if file_path is not None:
        grouped.to_csv(file_path)

    return grouped

def load_previous_year_war_table(file_path="data/historical_war_table.csv"):
    """Loads historical war table from a given file

    Args:
        file_path (str, optional): War file. Defaults to "data/historical_war_table.csv".

    Returns:
        pandas.DataFrame: War Table
    """
    return pd.read_csv(file_path, index_col=0)