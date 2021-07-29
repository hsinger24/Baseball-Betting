import pandas as pd

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

def _retrieve_offense_war_table(year):
    """Retrieves the offensive WAR table for a single year. Should not be used outside this file.

    Args:
        year (int): year to find war table

    Returns:
        pandas.DataFrame: The War table
    """
    year = str(year)
    offense_war_html = pd.read_html(
        f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season={year}&month=0&season1={year}&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=&enddate=')

    TEAM_WAR_TABLE_INDEX = 16

    # Find the correct table
    offense_war_table = offense_war_html[TEAM_WAR_TABLE_INDEX]

    # Set up dataframe by adjusting columns
    offense_war_table_columns = []
    for _, j in offense_war_table.columns:
        offense_war_table_columns.append(j)
    offense_war_table.columns = offense_war_table_columns
    offense_war_table_final = offense_war_table.loc[:, ['Team', 'WAR']]

    return offense_war_table_final

def _retrieve_defense_war_table(year):
    """Retrieves the Defensive WAR table. Should not be used outside this file

    Args:
        year (int): the year to retrieve the war table for

    Returns:
        pandas.DataFrame: The War table
    """
    year = str(year)
    TEAM_WAR_TABLE_INDEX = 16
    defense_war_html = pd.read_html(
        f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season={year}&month=0&season1={year}&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=&enddate=')

    # get the correct table
    defense_war_table = defense_war_html[TEAM_WAR_TABLE_INDEX]

    # set up dataframe by adjusting columns
    defense_war_table_columns = []
    for _, j in defense_war_table.columns:
        defense_war_table_columns.append(j)
    defense_war_table.columns = defense_war_table_columns
    defense_war_table_final = defense_war_table.loc[:, ['Team', 'WAR']]

    return defense_war_table_final

def retrieve_historical_combined_war_table(year, file_path="data/war_table.csv"):
    """Retrieves the Offensive and Defensive War tables for a given year (past) and saves it to a file,
    if the given file_path is not None

    Args:
        year (int): Year to get
        file_path (str, optional): path to save file. Defaults to "data/war_table.csv".

    Returns:
        pandas.DataFrame: The War table
    """
    # get both offense and defense tables
    offense_table = _retrieve_offense_war_table(year)
    defense_table = _retrieve_defense_war_table(year)

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

    if file_path is not None:
        with open(file_path, "w") as f:
            war.to_csv(f)

    return war

def load_combined_war_table(file_path="data/war_table.csv"):
    """Loads a War Table from a given file

    Args:
        file_path (str, optional): War file. Defaults to "data/war_table.csv".

    Returns:
        pandas.DataFrame: War Table
    """
    return pd.read_csv(file_path, index_col=0)



