import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime as dt
import pickle

_team_map_old = {
    'LA Dodgers' : 'Dodgers',
    'Minnesota': 'Twins',
    'Cincinnati': 'Reds',
    'Chi Sox' : 'White Sox',
    'Milwaukee' : 'Brewers',
    'Cleveland' : 'Indians',
    'St. Louis' : 'Cardinals',
    'San Diego': 'Padres',
    'Chi Cubs': 'Cubs',
    'Tampa Bay': 'Rays',
    'Atlanta': 'Braves',
    'Houston': 'Astros',
    'Oakland': 'Athletics',
    'SF Giants': 'Giants',
    'Kansas City': 'Royals',
    'Pittsburgh': 'Pirates',
    'Texas': 'Rangers',
    'NY Yankees': 'Yankees',
    'Baltimore': 'Orioles',
    'Seattle': 'Mariners',
    'LA Angels': 'Angels',
    'Toronto': 'Blue Jays',
    'NY Mets': 'Mets',
    'Miami': 'Marlins',
    'Arizona': 'Diamondbacks',
    'Detroit': 'Tigers',
    'Washington': 'Nationals',
    'Philadelphia': 'Phillies',
    'Colorado': 'Rockies',
    'Boston': 'Red Sox'
}

_team_map_new = {
    'LA Dodgers' : 'Dodgers',
    'Minnesota': 'Twins',
    'Cincinnati': 'Reds',
    'Chi Sox' : 'White Sox',
    'Milwaukee' : 'Brewers',
    'Cleveland' : 'Guardians',
    'St. Louis' : 'Cardinals',
    'San Diego': 'Padres',
    'Chi Cubs': 'Cubs',
    'Tampa Bay': 'Rays',
    'Atlanta': 'Braves',
    'Houston': 'Astros',
    'Oakland': 'Athletics',
    'SF Giants': 'Giants',
    'Kansas City': 'Royals',
    'Pittsburgh': 'Pirates',
    'Texas': 'Rangers',
    'NY Yankees': 'Yankees',
    'Baltimore': 'Orioles',
    'Seattle': 'Mariners',
    'LA Angels': 'Angels',
    'Toronto': 'Blue Jays',
    'NY Mets': 'Mets',
    'Miami': 'Marlins',
    'Arizona': 'Diamondbacks',
    'Detroit': 'Tigers',
    'Washington': 'Nationals',
    'Philadelphia': 'Phillies',
    'Colorado': 'Rockies',
    'Boston': 'Red Sox'
}

def _table_maker(link_list, year):
    '''
    Internal function to return the data needed for cluster luck analysis for a given year
    Params:
        - link_list: list of links to get the pitching data from the given year
        - year of interest
    Returns:
        - DF with all the relevant pitching data for CL analysis from a given year
    '''

    # Getting pitching data from given link
    table_list = []
    for i in link_list:
        dfs = pd.read_html(i)
        df = dfs[0]
        #df.drop(['Last 3', 'Last 1', 'Home', 'Away', prior_year], axis=1, inplace=True)
        df = df[['Rank', 'Team', str(year)]]
        table_list.append(df)

    # Merging the three tables
    df1 = pd.merge(left=table_list[0], right=table_list[1], on='Team')
    df2 = pd.merge(left=df1, right=table_list[2], on='Team')
    df2.drop(['Rank_x', 'Rank_y', 'Rank'], axis=1, inplace=True)
    df3 = pd.merge(left=df2, right=table_list[3], on='Team')
    pitching_table = pd.merge(left=df3, right=table_list[4], on='Team')
    pitching_table.drop(['Rank_x', 'Rank_y'], axis=1, inplace=True)
    pitching_table.columns = ['Team', 'SLG', 'OBP', 'ISO', 'RPG', 'HPG']
    pitching_table['HPR'] = pitching_table.HPG / pitching_table.RPG
    return pitching_table

def _retrieve_single_year_pitching_table(year):
    '''
    Internal function to return the pitching data for the inputted year
    Params:
        - year: year of interest
    Returns:
        - DF with pitching data from a given year
    '''

    # Generating links to feed into _table_maker()
    links = [f'https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date={year}-10-31', f'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date={year}-10-31',
                      f'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date={year}-10-31', f'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date={year}-10-31', f'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date={year}-10-31']
    pitching_data = pd.DataFrame()
    pitching_data = pitching_data.append(_table_maker(links, year))

    # Changing team name to be consistent
    if year < 2022:
        pitching_data.Team = pitching_data.Team.apply(lambda x: _team_map_old[x])
    else:
        pitching_data.Team = pitching_data.Team.apply(lambda x: _team_map_new[x])
    return pitching_data

def retrieve_historical_pitching_tables(years, file_name="data/historical_clusterluck_team_pitching.csv"):
    '''
    Retreives pitching data for one year, or a list of years
    Params:
        - years: years of interest
        - file_name: where to save the data. Defaults to data folder
    Returns:
        - DF with combined data from the inputted years
    '''

    # Putting data from all year(s) into one table
    pitching_data = pd.DataFrame()
    if type(years) is int:
        pitching_data = pitching_data.append(_retrieve_single_year_pitching_table(years))
    else:
        for year in years:
            pitching_data = pitching_data.append(_retrieve_single_year_pitching_table(year))

    # Saving file to CSV in data folder (by default)
    if file_name is not None:
        pitching_data.to_csv(file_name)
    
    
    return pitching_data

def load_historical_pitching_tables(file_name="data/historical_clusterluck_team_pitching.csv"):
    '''
    Loads historical pitching data table
    Params:
        - file_name: location to find historical pitching data
    Returns:
        - historical pitching data
    '''
    return pd.read_csv(file_name, index_col=0)

def calculate_and_save_pitching_linear_regression(previous_three_years_table, file_name='./data/pitching_regression.pickle'):
    '''
    Calculate and save CL regression for pitching from historical data
    Params:
        - previous_three_years_table: historical data to calculate regression from
        - file_name: location to save regression
    Returns:
        - regression for CL pitching
    '''

    # Getting relevant data and fitting linear regression
    x = previous_three_years_table.loc[:, ['SLG', 'OBP', 'ISO']]
    y = previous_three_years_table.HPR
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)

    # Saving regression to specified location
    if file_name is not None:
        with open(file_name, 'wb') as f:
            pickle.dump(linear_regression, f)

    return linear_regression

def calculate_predicted_cluster_luck_run_adjustment_pitching(linear_regression, pitching_data, gp=162):
    '''
    Calculate CL adjustment
    Params:
        - linear_regression: CL pitching regression calculated from historical data
        - pitching_data: the pitching data on which the regression will be applied
        - file_name: location to store the results
    Returns:
        - DF with predicted run adjustment
    '''
    pitching_data = pitching_data.copy()

    # Getting variables of interest and feeding into LR model for prediction
    x_vars = pitching_data.loc[:, ['SLG', 'OBP', 'ISO']]
    pitching_data['predict'] = linear_regression.predict(x_vars)

    # calculate runs and adjust columns
    pitching_data['R'] = pitching_data.RPG*gp
    pitching_data['run_adjust'] = (
        (pitching_data['predict'] - pitching_data['HPR']) / pitching_data['HPR'])*pitching_data['R']

    return pitching_data
