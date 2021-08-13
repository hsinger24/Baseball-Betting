import pandas as pd
import datetime as dt
import pickle


def calculate_preseason_win_percentage(cluster_luck_table, final_preseason_war_projections, current_year, file_name = None):
    # merge tables
    table = pd.merge(cluster_luck_table, final_preseason_war_projections, on='Team')

    # drop unnecessary columns
    drop_list_final = ['Runs', 'Offensive_Adjustment', 'Runs_Allowed',
                       'Defensive_Adjustment',
                       str(current_year), str(current_year-1)]
    table.drop(drop_list_final, axis=1, inplace=True)

    # use Pythagorean Linear Regression to predict win %
    table['Win_Percentage'] = .5 + 0.000683 * \
        (table.Adjusted_Runs_Scored + table.Run_Change - table.Adjusted_Runs_Allowed)
    
    if file_name is not None:
        table.to_csv(file_name)

    return table


