import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle


_team_map = {
    'New York Mets' : 'Mets',
    "Atlanta Braves": 'Braves',
    'Boston Red Sox': 'Red Sox',
    'Washington Nationals':  'Nationals',
    'San Francisco Giants':  'Giants',
    'Chicago White Sox': 'White Sox',
    'Baltimore Orioles' : 'Orioles',
    'Colorado Rockies' : 'Rockies',
    'Philadelphia Phillies': 'Phillies',
    'San Diego Padres': 'Padres',
    'Los Angeles Dodgers': 'Dodgers',
    'Toronto Blue Jays': 'Blue Jays',
    'Los Angeles Angels': 'Angels',
    'New York Yankees' : 'Yankees',
    'Detroit Tigers' : 'Tigers',
    'Kansas City Royals': 'Royals',
    'Miami Marlins': 'Marlins',
    'Minnesota Twins': 'Twins',
    'Arizona Diamondbacks': 'Diamondbacks',
    'Houston Astros': 'Astros',
    'Tampa Bay Rays': 'Rays',
    'St. Louis Cardinals': 'Cardinals',
    'Cleveland Indians': 'Indians',
    'Seattle Mariners': 'Mariners',
    'Oakland Athletics': 'Athletics',
    'Milwaukee Brewers': 'Brewers',
    'Chicago Cubs': 'Cubs',
    'Pittsburgh Pirates': 'Pirates',
    'Texas Rangers': 'Rangers',
    'Cincinnati Reds': 'Reds'
}

def _retrieve_single_year_hitting_table(year: int) -> pd.DataFrame:
    """Retrieves a table from espn for a team's single year cluster luck table with
    cluster luck regressors. This function should not be used outside this file

    Args:
        year (int): the year to retrieve

    Returns:
        pd.DataFrame: DataFrame containing a teams single year stats to be used for cluster lucks
    """
    # Link to espn
    link = 'https://www.espn.com/mlb/stats/team/_/stat/batting/season/%s/seasontype/2' % year

    # will hold combination of all stats for teams for given year
    hitting_table = pd.DataFrame()

    # Collect hitting table for given year
    stats_table_html = pd.read_html(year)
    # Combine two required tables
    combined_stats_table = pd.concat([stats_table_html[0], stats_table_html[1]], axis=1)
    hitting_table = hitting_table.append(combined_stats_table)

    # Convert Team names to standard naming convention
    hitting_table.Team = hitting_table.Team.apply(lambda x: _team_map[x])

    return hitting_table

def retrieve_historical_hitting_tables(years: list[int], file_name="data/historical_team_hitting.csv") -> pd.DataFrame:
    """Retrieve multi-year hitting table for a given list of years.

    Args:
        years (list[int]): the list of years to retrieve information from
        file_name(str, optional): The file_path to save the resulting DataFrame to. If None, will not save.
        Defaults to 'data/historical_team_hitting.csv'

    Returns:
        pd.DataFrame: a DataFrame containing the data to be used in a regression for clusterluck
    """
    # will hold combination of all stats for teams
    multi_year_hitting_table = pd.DataFrame()

    # loop through each year and append the single year table
    for year in years:
        multi_year_hitting_table.append(_retrieve_single_year_hitting_table(year))

    # sort and adjust and/or add columns
    multi_year_hitting_table.sort_values(by=['HR'], inplace=True, ascending=False)

    # Calculate ISO or isolated slugging to be used as a regressor
    multi_year_hitting_table['ISO'] = (multi_year_hitting_table['2B']+2*multi_year_hitting_table['3B'] +
                            3*multi_year_hitting_table['HR']) / multi_year_hitting_table['AB']
    # Calculate HPR or Hits per Run to be used as the predicted variable in regression
    multi_year_hitting_table['HPR'] = multi_year_hitting_table['H'] / multi_year_hitting_table['R']

    # If the file_name is not None then save the historical data to the given file
    if file_name is not None:
        with open(file_name, 'w') as f:
            multi_year_hitting_table.to_csv(f)

    return multi_year_hitting_table

def load_historical_hitting_tables(file_name="data/historical_team_hitting.csv") -> pd.DataFrame:
    """Loads a hitting table from a saved file.

    Args:
        file_name (str, optional): Path to load data from. Defaults to "data/historical_team_hitting.csv".

    Returns:
        pd.DataFrame: Historical hitting table
    """
    return pd.read_csv(file_name, index_col=0)

def calculate_and_save_hitting_linear_regression(previous_three_years_table: pd.DataFrame, file_name='./data/hitting_regression.pickle')->LinearRegression:
    """Runs a linear regression on Hits per Run based on team's previous years OBP, ISO and SLG.
    Stores results to a pickle file if file_name is not None. By defualt, saves results to data
    directory.

    Args:
        previous_three_years_table (pd.DataFrame): The DataFrame containing previous (three) years team data
        file_name (str, optional): File to save regression results to. If None, does not save results.
        Defaults to './data/hitting_regression.pickle'.

    Returns:
        LinearRegression: The Linear Regression object
    """
    # if load:
    #     with open("./beginning_scripts/hitting_regression.pickle", 'rb') as f:
    #         return pickle.load(f)
    
    # Setup x and y variables for regression
    x = previous_three_years_table.loc[:, ['OBP', 'ISO', 'SLG']]
    y = previous_three_years_table.HPR

    # create regression
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)
    
    # If file_name is none then do not save the regression
    if file_name is not None:
        with open(file_name, 'wb') as f:
            pickle.dump(linear_regression, f)

    return linear_regression

def calculate_predicted_cluster_luck_run_adjustment_hitting(linear_regression:LinearRegression, hitting_data:pd.DataFrame)->pd.DataFrame:
    """Constructs a DataFrame with the predicted HPR and the run adjustment based on a linear regression
    and hitting data.

    Args:
        linear_regression (LinearRegression): A linear regression that results from `calculate_and_save_hitting_linear_regression`
        hitting_data (pd.DataFrame): a hitting data table (usually from previous year) resulting from `retrieve_historical_hitting_tables(last_year)`

    Returns:
        pd.DataFrame: A DataFrame with the predicted HPR per team and cluster_luck run hitting adjustment per team
    """
    # Don't want to change original DataFrame so Make a copy for results
    prev_year_hitting = hitting_data.copy()

    # The X variables in the regression
    regression_x_vars = prev_year_hitting.loc[:, ['OBP', 'ISO', 'SLG']]
    # The prediction based on the regression
    prev_year_hitting['predict'] = linear_regression.predict(regression_x_vars)

    # Calculate the run adjustment column based on prediction
    prev_year_hitting['run_adjust'] = ( (prev_year_hitting['HPR'] - prev_year_hitting['predict']) / prev_year_hitting['HPR']) * prev_year_hitting['R']

    return prev_year_hitting

    



