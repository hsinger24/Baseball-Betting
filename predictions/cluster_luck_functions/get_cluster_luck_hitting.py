import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime as dt
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

def get_prev_three_years_hitting_table():
    # last three years links

    current_year = dt.date.today().year
    years = [str(current_year-2), str(current_year-3), str(current_year-4)]
    

    # list of links to espn
    links = ['https://www.espn.com/mlb/stats/team/_/stat/batting/season/%s/seasontype/2' % (year) for year in years]

    #links = ['https://www.espn.com/mlb/stats/team/_/stat/batting', 'https://www.espn.com/mlb/stats/team/_/stat/batting/season/2018/seasontype/2',
    #         'https://www.espn.com/mlb/stats/team/_/stat/batting/season/2017/seasontype/2']

    # will hold combination of all stats for teams from
    #   previous three years
    hitting_table = pd.DataFrame()

    # loop through each year
    for year in links:
        stats_table_html = pd.read_html(year)
        combined_stats_table = pd.concat(
            [stats_table_html[0], stats_table_html[1]], axis=1)
        hitting_table = hitting_table.append(combined_stats_table)

    # sort and adjust and/or add columns
    hitting_table.sort_values(by=['HR'], inplace=True, ascending=False)
    hitting_table['ISO'] = (hitting_table['2B']+2*hitting_table['3B'] +
                            3*hitting_table['HR']) / hitting_table['AB']
    hitting_table['HPR'] = hitting_table['H'] / hitting_table['R']

    return hitting_table


def get_hitting_linear_regression(previous_three_years_table, load=True):
    if load:
        with open("./beginning_scripts/hitting_regression.pickle", 'rb') as f:
            return pickle.load(f)
    
    # setup x and y variables for regression
    x = previous_three_years_table.loc[:, ['OBP', 'ISO', 'SLG']]
    y = previous_three_years_table.HPR

    # create regression
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)
    
    
    with open('./beginning_scripts/hitting_regression.pickle', 'wb') as f:
        pickle.dump(linear_regression, f)

    return linear_regression


def get_prev_year_hitting_table(linear_regression):
    # TODO get prev_year automatically
    prev_year = dt.date.today().year - 1
    # pull the html for last years stats

    url_last_year ='https://www.espn.com/mlb/stats/team/_/stat/batting/season/%s/seasontype/2' % prev_year
    prev_year_hitting_html = pd.read_html(url_last_year)

    # combine the tables accordingly
    prev_year_hitting = pd.concat(
        [prev_year_hitting_html[0], prev_year_hitting_html[1]], axis=1)

    # add stats columns
    prev_year_hitting['ISO'] = (prev_year_hitting['2B']+2*prev_year_hitting['3B'] +
                                3*prev_year_hitting['HR']) / prev_year_hitting['AB']
    prev_year_hitting['HPR'] = prev_year_hitting['H'] / prev_year_hitting['R']

    # predict hits per run from regression
    regression_x_vars = prev_year_hitting.loc[:, ['OBP', 'ISO', 'SLG']]
    prev_year_hitting['predict'] = linear_regression.predict(regression_x_vars)

    # add a run adjustment column based on prediction
    prev_year_hitting['run_adjust'] = (
        (prev_year_hitting['HPR'] - prev_year_hitting['predict']) / prev_year_hitting['HPR'])*prev_year_hitting['R']

    # add a team name row accordingly
    # team_list = ['Astros', 'Twins', 'Red Sox', 'Yankees', 'Rockies', 'Nationals', 'Pirates', 'White Sox', 'Braves', 'Dodgers', 'Mets', 'Rays', 'Cubs', 'Diamondbacks',
    #              'Indians', 'Athletics', 'Rangers', 'Angels', 'Royals', 'Brewers', 'Orioles', 'Phillies', 'Cardinals', 'Reds', 'Marlins', 'Tigers', 'Giants', 'Padres', 'Mariners', 'Blue Jays']
    # prev_year_hitting['Team'] = team_list

    prev_year_hitting.Team = prev_year_hitting.Team.apply(lambda x: _team_map[x])

    return prev_year_hitting


def get_cluster_luck_hitting_table():
    previous_three_years_hitting_table = get_prev_three_years_hitting_table()
    linear_regression_hitting = get_hitting_linear_regression(
        previous_three_years_hitting_table)
    cluster_luck_hitting_table = get_prev_year_hitting_table(
        linear_regression_hitting)

    return cluster_luck_hitting_table

def get_cluster_luck_hitting_current_year():
    current_year = dt.date.today().year
    url_this_year = 'https://www.espn.com/mlb/stats/team/_/stat/batting/season/%s/seasontype/2' % current_year
    current_year_html = pd.read_html(url_this_year)
    current_year_hitting = pd.concat(
        [current_year_html[0], current_year_html[1]], axis=1)
    current_year_hitting['ISO'] = (current_year_hitting['2B']+2*current_year_hitting['3B'] +
                                3*current_year_hitting['HR']) / current_year_hitting['AB']
    current_year_hitting['HPR'] = current_year_hitting['H'] / current_year_hitting['R']
    regression = get_hitting_linear_regression(get_prev_three_years_hitting_table())
    regression_x_vars = current_year_hitting.loc[:, ['OBP', 'ISO', 'SLG']]
    current_year_hitting['predict'] = regression.predict(regression_x_vars)
    current_year_hitting['run_adjust'] = (
        (current_year_hitting['HPR'] - current_year_hitting['predict']) / current_year_hitting['HPR'])*current_year_hitting['R']
    current_year_hitting.Team = current_year_hitting.Team.apply(lambda x: _team_map[x])
    return current_year_hitting
    



