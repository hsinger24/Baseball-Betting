from bs4 import BeautifulSoup
from lxml import html
import requests
import re

# Get the html for the games and their info for the day
page = requests.get(
    'https://www.fangraphs.com/roster-resource/depth-charts/angels')
soup = BeautifulSoup(page.content, 'lxml')

players = soup.find_all('td', data-stat='cell-painted roster-40')
print(players)
for player in players:
    print(player)
