import pandas as pd
from sklearn.linear_model import LinearRegression


def get_prev_three_years_hitting_table():
    # last three years links
    links = ['https://www.espn.com/mlb/stats/team/_/stat/batting', 'https://www.espn.com/mlb/stats/team/_/stat/batting/season/2018/seasontype/2',
             'https://www.espn.com/mlb/stats/team/_/stat/batting/season/2017/seasontype/2']

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


def get_hitting_linear_regression(previous_three_years_table):
    # setup x and y variables for regression
    x = previous_three_years_table.loc[:, ['OBP', 'ISO', 'SLG']]
    y = previous_three_years_table.HPR

    # create regression
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)

    return linear_regression


def get_prev_year_hitting_table(linear_regression):
    # pull the html for last years stats
    prev_year_hitting_html = pd.read_html(
        'https://www.espn.com/mlb/stats/team/_/stat/batting')

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
    team_list = ['Astros', 'Twins', 'Red Sox', 'Yankees', 'Rockies', 'Nationals', 'Pirates', 'White Sox', 'Braves', 'Dodgers', 'Mets', 'Rays', 'Cubs', 'Diamondbacks',
                 'Indians', 'Athletics', 'Rangers', 'Angels', 'Royals', 'Brewers', 'Orioles', 'Phillies', 'Cardinals', 'Reds', 'Marlins', 'Tigers', 'Giants', 'Padres', 'Mariners', 'Blue Jays']
    prev_year_hitting['Team'] = team_list

    return prev_year_hitting


def get_cluster_luck_hitting_table():
    previous_three_years_hitting_table = get_prev_three_years_hitting_table()
    linear_regression_hitting = get_hitting_linear_regression(
        previous_three_years_hitting_table)
    cluster_luck_hitting_table = get_prev_year_hitting_table(
        linear_regression_hitting)

    return cluster_luck_hitting_table
