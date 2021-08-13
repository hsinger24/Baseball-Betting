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
import unidecode

def retrieve_current_year_WAR(file_path = "data/curr_war_table.csv"):
    """Retrieves the current year WAR of all players who have played in the MLB this season from 
    baseball prospectus

    Args:
        file_path (str, optional): path to save file. Defaults to "data/curr_war_table.csv".

    Returns:
        pandas.DataFrame: The current year war table
    """
    driver = webdriver.Chrome('../chromedriver')
    driver.get('https://www.baseballprospectus.com/leaderboards/hitting/')
    regex_name = r'(\D+\s\D+)+'
    table_dict = {}
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
            time.sleep(2)
            plate_appearance_input = driver.find_element_by_name('currentSliderValue')
            plate_appearance_input.clear()
            plate_appearance_input.send_keys('0')
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[5]/div/div/div/div[2]/button[2]")
            save_button.click()
            time.sleep(2)
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
            time.sleep(2)
            team_filter.click()
            time.sleep(2)
            team_options = driver.find_elements_by_class_name('multi-select__box')
            team_options[i].click()
            team_options[(i+1)].click()
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[4]/div/div/div/div[2]/button[2]")
            save_button.click()
            time.sleep(2)
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
            time.sleep(2)
            innings_input = driver.find_element_by_name('currentSliderValue')
            innings_input.clear()
            innings_input.send_keys('0')
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[5]/div/div/div/div[2]/button[2]")
            save_button.click()
            time.sleep(2)
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
            time.sleep(2)
            team_filter.click()
            time.sleep(2)
            team_options = driver.find_elements_by_class_name('multi-select__box')
            team_options[i].click()
            team_options[(i+1)].click()
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[4]/div/div/div/div[2]/button[2]")
            save_button.click()
            time.sleep(2)
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
    all_players = pd.DataFrame()
    for key, value in table_dict.items():
        all_players = all_players.append(value)
    def conv(x):
        try:
            return float(x)
        except:
            return 0
    all_players['WAR'] = all_players['WAR'].apply(conv)
    grouped = all_players.groupby(by = 'Name')['WAR'].sum()
    grouped = pd.DataFrame(grouped)
    grouped.reset_index(inplace = True)
    grouped.columns = ['Name', 'WAR']
    grouped['Name'] = grouped.Name.apply(unidecode.unidecode)

    if file_path is not None:
        with open("data/curr_war_table.csv", 'w') as f:
            grouped.to_csv(f)

    return grouped

def load_current_year_WAR(file_path = "data/curr_war_table.csv"):
    """Loads the current year war Table from a given file

    Args:
        file_path (str, optional): War file. Defaults to "data/curr_war_table.csv".

    Returns:
        pandas.DataFrame: Current year War Table
    """

    return pd.read_csv(file_path, index_col = 0)

def retrieve_historical_player_war_tables(driver, year):
    for i in range(2):
        if i == 1:
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
        if str(year) != year_current:

            # set the year to the given year
            year_filter.click()
            year_slider = driver.find_element_by_name("currentSliderValue")
            year_slider.clear()
            year_slider.send_keys(year)

            # get the save button, click it and wait for it to be stale
            save_btn = driver.find_elements_by_class_name("modal__btn--save")[0]
            save_btn.click()
            WebDriverWait(driver, 10).until(EC.staleness_of(save_btn))

        # Set PA/IP to 0    
        plate_apearance_innings_pitched_filter = filters[4]
        plate_apearance_innings_pitched_filter.click()
        pa_slider = driver.find_element_by_name("currentSliderValue")
        pa_slider.clear()
        pa_slider.send_keys(0)

        # save selection
        save_btn = driver.find_elements_by_class_name("modal__btn--save")[0]
        save_btn.click()
        WebDriverWait(driver, 10).until(EC.staleness_of(save_btn))

        # unclick the default all selection
        team_filter = filters[3]
        team_filter.click()
        teams = driver.find_elements_by_class_name("multi-select__box")
        all_btn = teams[0]
        all_btn.click()

        # create dict to store team's player tables
        table_dict = {}
        regex_name = r'(\D+\s\D+)+'

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
            WebDriverWait(driver, 10).until(
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
            hitting_table = pd.read_html(html)
            hitting_table = hitting_table[0]
            hitting_table = hitting_table.iloc[0:(hitting_table.shape[0]), [0,2,3]]
            hitting_table.columns = ['Name', 'Team', 'WAR']

            hitting_table['Name'] = hitting_table.Name.apply(lambda x: re.findall(regex_name, x)[0])
            hitting_table['Name'] = hitting_table.Name.apply(lambda x: x.strip(' '))

            hitting_table['WAR'] = hitting_table.WAR.apply(to_num)

            team_name = hitting_table.iloc[0,1]
            table_dict[team_name] = pd.DataFrame(columns = hitting_table.columns)
            table_dict[team_name] = table_dict[team_name].append(hitting_table)

            print(team_name)

            # Unclick the team
            team_filter.click()
            team_btn = driver.find_elements_by_class_name("multi-select__box")[i]
            team_btn.click()
        
        
    return table_dict