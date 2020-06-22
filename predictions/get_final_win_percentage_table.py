import pandas as pd


def get_win_percentage_predictions(cluster_luck_table, war_table):
    # merge tables
    table = pd.merge(cluster_luck_table, war_table, on='Team')

    # drop unnecessary columns
    drop_list_final = ['Runs', 'Offensive_Adjustment', 'Runs_Allowed',
                       'Defensive_Adjustment',
                       '2020', '2019']
    table.drop(drop_list_final, axis=1, inplace=True)

    # use Pythagorean Linear Regression to predict win %
    table['Win_Percentage'] = .5 + 0.000683 * \
        (table.Adjusted_Runs_Scored + table.Run_Change - table.Adjusted_Runs_Allowed)

    return table
