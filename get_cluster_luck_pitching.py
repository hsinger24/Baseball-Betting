import pandas as pd
from sklearn.linear_model import LinearRegression


def table_maker(link_list, prior_year):
    table_list = []
    for i in link_list:
        dfs = pd.read_html(i)
        df = dfs[0]
        df.drop(['Last 3', 'Last 1', 'Home', 'Away',
                 prior_year], axis=1, inplace=True)
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
    link_list_2019 = ['https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date=2019-10-31', 'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date=2019-10-31',
                      'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date=2019-10-31', 'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date=2019-10-31', 'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date=2019-10-31']
    table_2019 = table_maker(link_list_2019, '2018')
    link_list_2018 = ['https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date=2018-10-29',
                      'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date=2018-10-29', 'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date=2018-10-29']
    link_list_2017 = ['https://www.teamrankings.com/mlb/stat/opponent-slugging-pct?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-on-base-pct?date=2017-11-02',
                      'https://www.teamrankings.com/mlb/stat/opponent-isolated-power?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-runs-per-game?date=2017-11-02', 'https://www.teamrankings.com/mlb/stat/opponent-hits-per-game?date=2017-11-02']
    table_2018 = table_maker(link_list_2018, '2017')
    table_2017 = table_maker(link_list_2017, '2016')
    t1 = table_2019.append(table_2018)
    pitching_data = t1.append(table_2017)

    return pitching_data, table_2019


def get_pitching_linear_regression(pitching_data):
    # Linear Regression for Pitching
    X_pitching = pitching_data.loc[:, ['SLG', 'OBP', 'ISO']]
    Y_pitching = pitching_data.HPR
    lr_pitching = LinearRegression()
    lr_pitching.fit(X_pitching, Y_pitching)

    return lr_pitching


def get_previous_year_pitching_table(lr_pitching, table_2019):
    # Creating 2019 Pitching Table With CL Adjustments
    pitching_2019_x = table_2019.loc[:, ['SLG', 'OBP', 'ISO']]
    table_2019['predict'] = lr_pitching.predict(pitching_2019_x)
    table_2019['R'] = table_2019.RPG*162
    table_2019['run_adjust'] = (
        (table_2019['predict'] - table_2019['HPR'])/table_2019['HPR'])*table_2019['R']
    team_list = ['Dodgers', 'Rays', 'Cardinals', 'Astros', 'Athletics', 'Reds', 'Nationals', 'Cubs', 'Mets', 'Indians', 'Braves', 'Twins', 'Brewers', 'Giants', 'Padres',
                 'Red Sox', 'Diamondbacks', 'Yankees', 'Marlins', 'Blue Jays', 'White Sox', 'Phillies', 'Royals', 'Angels', 'Rangers', 'Mariners', 'Pirates', 'Tigers', 'Rockies', 'Orioles']
    table_2019['Team'] = team_list

    return table_2019


def get_cluster_luck_pitching_table():
    pitching_data, table_2019 = get_prev_three_years_stats()
    lr_pitching = get_pitching_linear_regression(pitching_data)
    cluster_luck_pitching_table = get_previous_year_pitching_table(
        lr_pitching, table_2019)

    return cluster_luck_pitching_table
