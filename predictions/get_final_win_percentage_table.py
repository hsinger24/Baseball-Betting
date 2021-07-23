import pandas as pd
import datetime as dt
import pickle


def get_win_percentage_predictions(cluster_luck_table, war_table, save=False):
    current_year = dt.date.today().year
    # merge tables
    table = pd.merge(cluster_luck_table, war_table, on='Team')

    # drop unnecessary columns
    drop_list_final = ['Runs', 'Offensive_Adjustment', 'Runs_Allowed',
                       'Defensive_Adjustment',
                       str(current_year), str(current_year-1)]
    table.drop(drop_list_final, axis=1, inplace=True)

    # use Pythagorean Linear Regression to predict win %
    table['Win_Percentage'] = .5 + 0.000683 * \
        (table.Adjusted_Runs_Scored + table.Run_Change - table.Adjusted_Runs_Allowed)
    
    if save:
        with open("./beginning_scripts/baseline_win_perc.pickle", "wb") as f:
            pickle.dump(table, f)

    return table


def access_baseline_win_percentage_predictions():
    with open("./beginning_scripts/baseline_win_perc.pickle", "rb") as f:
        return pickle.load(f)
