from bs4 import BeautifulSoup
from lxml import html
import requests
import re


def get_todays_games_info():
    # Get the html for the games and their info for the day
    page = requests.get('https://www.mlb.com/starting-lineups')
    soup = BeautifulSoup(page.content, 'lxml')

    # Array of games to store all the information about the game
    games = []

    # Get team names
    teams = soup.find_all('a', class_='starting-lineups__team-name--link')
    home_team = True
    game_num = 0
    for team in teams:
        if home_team:
            games.append({
                'home_team': {
                    'team_name': team.contents[0].strip(),
                    'starting_pitcher': '',
                    'lineup': []
                },
                'away_team': {
                    'team_name': '',
                    'starting_pitcher': '',
                    'lineup': []
                }
            })
        else:
            games[game_num]['away_team']['team_name'] = team.contents[0].strip()
            game_num += 1
        home_team = not home_team

    # Get the lineups for every team

    players = soup.find_all('a', class_='starting-lineups__player--link')
    counter = 0
    game_num = 0

    # to keep track of the 18 players in a game (first 9 are home, second 9 away)
    game_player_counter = 0

    for player in players:
        game_num = int(counter / 36)
        if int(counter / 18) % 2 is 0:
            if game_player_counter < 9:
                games[game_num]['home_team']['lineup'].append(
                    player.contents[0])
            else:
                games[game_num]['away_team']['lineup'].append(
                    player.contents[0])
            game_player_counter += 1
        else:
            game_player_counter = 0
        counter += 1

    # Get the starting pitchers for every team
    pitchers = soup.find_all('a', class_='starting-lineups__pitcher--link')
    game_num = 0
    home_team = True
    pitcher_name_is_here = False
    for pitcher in pitchers:
        if pitcher_name_is_here:
            if home_team:
                games[game_num]['home_team']['starting_pitcher'] = pitcher.contents[0]
            else:
                games[game_num]['away_team']['starting_pitcher'] = pitcher.contents[0]
                game_num += 1
            home_team = not home_team
        pitcher_name_is_here = not pitcher_name_is_here

    return games
