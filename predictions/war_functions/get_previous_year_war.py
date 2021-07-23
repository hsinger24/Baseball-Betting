import pandas as pd
import datetime as dt

team_map = {
    'LAD': 'Dodgers',
    'SDP': 'Padres',
    'CHW': 'White Sox',
    'MIN': 'Twins',
    'CLE': 'Indians',
    'OAK': 'Athletics',
    'TBR': 'Rays',
    'NYY': 'Yankees',
    'ATL': 'Braves',
    'NYM': 'Mets',
    'CHC': 'Cubs',
    'CIN': 'Reds',
    'LAA': 'Angels',
    'MIL': 'Brewers',
    'SFG': 'Giants',
    'PHI': 'Phillies',
    'HOU': 'Astros',
    'STL': 'Cardinals',
    'KCR': 'Royals',
    'BAL': 'Orioles',
    'SEA': 'Mariners',
    'TOR': 'Blue Jays',
    'DET': 'Tigers',
    'BOS': 'Red Sox',
    'ARI': 'Diamondbacks',
    'WSN': 'Nationals',
    'COL': 'Rockies',
    'MIA': 'Marlins',
    'PIT': 'Pirates',
    'TEX': 'Rangers'
}

def get_offense_previous_year_war_table():
    
    current_year = dt.date.today().year
    last_year = str(current_year-1)
    # import fangraphs html
    offense_war_html = pd.read_html(
        f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season={last_year}&month=0&season1={last_year}&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=&enddate=')

    TEAM_WAR_TABLE_INDEX = 16

    # get the correct table
    offense_war_table = offense_war_html[TEAM_WAR_TABLE_INDEX]

    # set up dataframe by adjusting columns
    offense_war_table_columns = []
    for _, j in offense_war_table.columns:
        offense_war_table_columns.append(j)
    offense_war_table.columns = offense_war_table_columns
    offense_war_table_final = offense_war_table.loc[:, ['Team', 'WAR']]

    return offense_war_table_final


def get_defense_previous_year_war_table():
    # import fangraphs html
    current_year = dt.date.today().year
    last_year = str(current_year-1)
    TEAM_WAR_TABLE_INDEX = 16
    defense_war_html = pd.read_html(
        f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season={last_year}&month=0&season1={last_year}&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=&enddate=')

    # get the correct table
    defense_war_table = defense_war_html[TEAM_WAR_TABLE_INDEX]

    # set up dataframe by adjusting columns
    defense_war_table_columns = []
    for _, j in defense_war_table.columns:
        defense_war_table_columns.append(j)
    defense_war_table.columns = defense_war_table_columns
    defense_war_table_final = defense_war_table.loc[:, ['Team', 'WAR']]

    return defense_war_table_final


def get_combined_previous_year_war_table():
    # get both offense and defense tables
    offense_table = get_offense_previous_year_war_table()
    defense_table = get_defense_previous_year_war_table()

    # merge tables
    war = pd.merge(offense_table, defense_table, on='Team')

    # adjust columns and create a total war column
    war.columns = ['Team', 'Offense', 'Defense']
    war.drop(30, inplace=True)
    war.Offense = pd.to_numeric(war['Offense'])
    war.Defense = pd.to_numeric(war.Defense)
    war['Total'] = war.Offense + war.Defense
    war.sort_values(by='Total', ascending=False, inplace=True)
    war.Team = war.Team.apply(lambda x: team_map[x])

    return war






