import pandas as pd
import re


def get_starting_rotations(pecota_table):
    team_list_links = ['https://www.lineups.com/mlb/depth-charts/arizona-diamondbacks', 'https://www.lineups.com/mlb/depth-charts/atlanta-braves',
                       'https://www.lineups.com/mlb/depth-charts/baltimore-orioles', 'https://www.lineups.com/mlb/depth-charts/boston-red-sox',
                       'https://www.lineups.com/mlb/depth-charts/chicago-cubs', 'https://www.lineups.com/mlb/depth-charts/chicago-white-sox',
                       'https://www.lineups.com/mlb/depth-charts/cincinnati-reds', 'https://www.lineups.com/mlb/depth-charts/cleveland-indians',
                       'https://www.lineups.com/mlb/depth-charts/colorado-rockies', 'https://www.lineups.com/mlb/depth-charts/detroit-tigers',
                       'https://www.lineups.com/mlb/depth-charts/houston-astros', 'https://www.lineups.com/mlb/depth-charts/kansas-city-royals',
                       'https://www.lineups.com/mlb/depth-charts/los-angeles-angels', 'https://www.lineups.com/mlb/depth-charts/los-angeles-dodgers',
                       'https://www.lineups.com/mlb/depth-charts/miami-marlins', 'https://www.lineups.com/mlb/depth-charts/milwaukee-brewers',
                       'https://www.lineups.com/mlb/depth-charts/minnesota-twins', 'https://www.lineups.com/mlb/depth-charts/new-york-mets',
                       'https://www.lineups.com/mlb/depth-charts/new-york-mets', 'https://www.lineups.com/mlb/depth-charts/oakland-athletics',
                       'https://www.lineups.com/mlb/depth-charts/philadelphia-phillies', 'https://www.lineups.com/mlb/depth-charts/pittsburgh-pirates',
                       'https://www.lineups.com/mlb/depth-charts/san-diego-padres', 'https://www.lineups.com/mlb/depth-charts/san-francisco-giants',
                       'https://www.lineups.com/mlb/depth-charts/seattle-mariners', 'https://www.lineups.com/mlb/depth-charts/st-louis-cardinals',
                       'https://www.lineups.com/mlb/depth-charts/tampa-bay-rays', 'https://www.lineups.com/mlb/depth-charts/tampa-bay-rays',
                       'https://www.lineups.com/mlb/depth-charts/toronto-blue-jays', 'https://www.lineups.com/mlb/depth-charts/washington-nationals']

    team_list = ['Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'Cubs', 'White Sox', 'Reds', 'Indians', 'Rockies',
                 'Tigers', 'Astros', 'Royals', 'Angels', 'Dodgers', 'Marlins', 'Brewers', 'Twins', 'Mets', 'Yankees',
                 'Athletics', 'Phillies', 'Pirates', 'Padres', 'Giants', 'Mariners', 'Cardinals', 'Rays', 'Rangers',
                 'Blue Jays', 'Nationals']

    # where every team's rotation will be stored
    starting_rotations = {}

    # iterate through all the links
    for index, link in enumerate(team_list_links):

        # get the depth chart table related to starting pitching
        table = pd.read_html(link)[1]

        # cast column to a string
        table['Position'] = table['Position'].astype('string')

        # get only the starting rotation
        subset = table[table['Position'] == 'Rotation  SP']

        # adjust columns
        subset.drop('Position', axis=1, inplace=True)
        subset.reset_index(inplace=True)
        subset.drop('index', axis=1, inplace=True)

        # more manipulating data to get the starting rotation
        sp_list = list(subset.iloc[0, :])
        sp = []
        for j in sp_list:
            regex = r'^\S+\s\S+'
            pitch = re.findall(regex, j)
            if pitch:
                sp.append(pitch[0])
        starting_rotations.update({team_list[index]: sp})

    # creating tables from the starting rotations
    starting_rotations_tables = {}
    failed_to_find_war_list = []
    for index, team in enumerate(team_list):
        table = pd.DataFrame(columns=['Name', 'WAR'])
        for index2, pitcher in enumerate(starting_rotations[team]):
            table.loc[index2, 'Name'] = pitcher
            try:
                table.loc[index2, 'WAR'] = pecota_table[pecota_table['name']
                                                        == pitcher]['war_162'].iloc[0]
            except:
                table.loc[index2, 'WAR'] = 0
                failed_to_find_war_list.append(pitcher)
        starting_rotations_tables[team] = table

    return starting_rotations_tables, failed_to_find_war_list
