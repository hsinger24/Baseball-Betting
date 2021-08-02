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

### NEED TO PUT IN FUNCTION###


# Get all current year WAR data by player

def _retrieve_current_year_WAR():
    driver = webdriver.Chrome('../Desktop/chromedriver')
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
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn'))).click()
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'load-more__btn')))
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
        else:
            time.sleep(1)
            team_filter.click()
            time.sleep(1)
            team_options = driver.find_elements_by_class_name('multi-select__box')
            team_options[i].click()
            team_options[(i+1)].click()
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[4]/div/div/div/div[2]/button[2]")
            save_button.click()
            time.sleep(1)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn'))).click()
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
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
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn'))).click()
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
            except:
                pass
            html = driver.page_source
            html = driver.page_source
            pitching_table = pd.read_html(html)
            pitching_table = pitching_table[0]
            pitching_table = pitching_table.iloc[0:(pitching_table.shape[0]), [0,2,3]]
            pitching_table.columns = ['Name', 'Team', 'WAR']
            pitching_table['Name'] = pitching_table.Name.apply(lambda x: re.findall(regex_name, x)[0])
            pitching_table['Name'] = pitching_table.Name.apply(lambda x: x.strip(' '))
            team_name = pitching_table.iloc[0,1]
            table_dict[team_name] = table_dict[team_name].append(pitching_table)
        else:
            time.sleep(1)
            team_filter.click()
            time.sleep(1)
            team_options = driver.find_elements_by_class_name('multi-select__box')
            team_options[i].click()
            team_options[(i+1)].click()
            save_button = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[4]/div/div/div/div[2]/button[2]")
            save_button.click()
            time.sleep(1)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn'))).click()
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more__btn')))
                time.sleep(0.5)
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
    return table_dict