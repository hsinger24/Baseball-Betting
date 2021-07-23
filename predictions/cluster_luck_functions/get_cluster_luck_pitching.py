import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime as dt
import pickle

_team_map = {
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


def table_maker(link_list, year):
    table_list = []
    for i in link_list:
        dfs = pd.read_html(i)
        df = dfs[0]
        #df.drop(['Last 3', 'Last 1', 'Home', 'Away', prior_year], axis=1, inplace=True)
        df = df[['Rank', 'Team', year]]
        table_list.append(df)

    df1 = pd.merge(left=table_list[0], right=table_list[1], on='Team')
    df2 = pd.merge(left=df1, right=table_list[2], on='Team')
    df2.drop(['Rank_x', 'Rank_y', 'Rank'], axis=1, inplace=True)
    df3 = pd.merge(left=df2, right=table_list[3], on='Team')
    pitching_table = pd.merge(left=df3, right=table_list[4], on='Team')
    pitching_table.drop(['Rank_x', 'Rank_y'], axis=1, inplace=True)
    pitching_table.columns = ['Team', 'SLG', 'OBP', 'ISO', 'RPG', 'HPG']
    pitching_table['HPR'] = pitching_table.HPG / pitching_table.RPG
    return pitching_table


def get_prev_three_years_stats():

    current_year = dt.date.today().year
    years = [str(current_year-2), str(current_year-3), str(current_year-4)]
    
    last_year = str(current_year-1)

    # LAST YEAR
    # create list of links for last year's data
    last_year_list = [f'https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date={last_year}-10-31', f'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date={last_year}-10-31',
                      f'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date={last_year}-10-31', f'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date={last_year}-10-31', f'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date={last_year}-10-31']
    # create dataframe for last year
    table_last = table_maker(last_year_list, last_year)

    # PREV 3 YEARS
    # for each of the previous years
    # get the list of links,
    pitching_data = pd.DataFrame()
    for year in years:
        one_year_list = [f'https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date={year}-10-31', f'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date={year}-10-31',
                      f'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date={year}-10-31', f'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date={year}-10-31', f'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date={year}-10-31']
        pitching_data = pitching_data.append(table_maker(one_year_list, year))

    #link_list_2019 = ['https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date=2019-10-31', 'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date=2019-10-31','https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date=2019-10-31', 'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date=2019-10-31', 'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date=2019-10-31']
    #table_2019 = table_maker(link_list_2019, '2018')
    #link_list_2018 = ['https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date=2018-10-29']
    #link_list_2017 = ['https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date=2017-11-02']
    #table_2018 = table_maker(link_list_2018, '2017')
    #table_2017 = table_maker(link_list_2017, '2016')
    #t1 = table_2019.append(table_2018)
    #pitching_data = t1.append(table_2017)

    return pitching_data, table_last


def get_pitching_linear_regression(pitching_data, load=True):
    if load:
        with open('./beginning_scripts/pitching_regression.pickle', 'rb') as f:
            return pickle.load(f)

    # Linear Regression for Pitching
    x = pitching_data.loc[:, ['SLG', 'OBP', 'ISO']]
    y = pitching_data.HPR
    linear_regression = LinearRegression()
    linear_regression.fit(x, y)

    with open('./beginning_scripts/pitching_regression.pickle', 'wb') as f:
        pickle.dump(linear_regression, f)

    return linear_regression


def get_previous_year_pitching_table(linear_regression, prev_year_table, gp=162):
    # use linear regression for prediction
    x_vars = prev_year_table.loc[:, ['SLG', 'OBP', 'ISO']]
    prev_year_table['predict'] = linear_regression.predict(x_vars)

    # calculate runs and adjust columns
    prev_year_table['R'] = prev_year_table.RPG*gp
    prev_year_table['run_adjust'] = (
        (prev_year_table['predict'] - prev_year_table['HPR']) / prev_year_table['HPR'])*prev_year_table['R']

    # add the team names as a column
    #team_list = ['Dodgers', 'Rays', 'Cardinals', 'Astros', 'Athletics', 'Reds', 'Nationals', 'Cubs', 'Mets', 'Indians', 'Braves', 'Twins', 'Brewers', 'Giants', 'Padres', 'Red Sox', 'Diamondbacks', 'Yankees', 'Marlins', 'Blue Jays', 'White Sox', 'Phillies', 'Royals', 'Angels', 'Rangers', 'Mariners', 'Pirates', 'Tigers', 'Rockies', 'Orioles']
    #prev_year_table['Team'] = team_list

    prev_year_table.Team = prev_year_table.Team.apply(lambda x: _team_map[x])

    return prev_year_table


def get_cluster_luck_pitching_table():
    prev_three_years_table, prev_year_table = get_prev_three_years_stats()
    pitching_linear_regression = get_pitching_linear_regression(
        prev_three_years_table)
    # TODO games played in 2020 was 60
    cluster_luck_pitching_table = get_previous_year_pitching_table(
        pitching_linear_regression, prev_year_table, gp=60)

    return cluster_luck_pitching_table



