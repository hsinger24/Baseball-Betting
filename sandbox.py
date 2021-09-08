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
log_in_email = browser.find_element_by_xpath("//*[@id='email-login-button']")
log_in_email.click()
email = browser.find_element_by_xpath("//*[@id='email-login-form']/div[2]/input")
email.click()
email.send_keys('singerfam1@gmail.com')
password = browser.find_element_by_xpath("//*[@id='email-login-form']/div[3]/input")
password.click()
password.send_keys('Tredwell01!')
log_in = browser.find_element_by_xpath("//*[@id='email-login-form']/button")
log_in.click()