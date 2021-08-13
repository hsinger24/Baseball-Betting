import pandas as pd
import datetime as dt
import pickle

def load_linear_regression(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

def merge_cluster_luck_tables(hitting_table, pitching_table, file_name=None):
    cluster_final = pd.merge(hitting_table, pitching_table, on='Team')
    # adjust columns
    drop_list = ['RK', 'GP', 'AB', 'H', '2B', '3B', 'HR', 'RBI', 'TB',
                 'BB', 'SO', 'SB', 'AVG', 'OBP_x', 'SLG_x', 'OPS', 'ISO_x', 'HPR_x',
                 'predict_x', 'SLG_y', 'OBP_y', 'ISO_y', 'RPG', 'HPG',
                 'HPR_y', 'predict_y', ]
    cluster_final.drop(drop_list, axis=1, inplace=True)
    cluster_final.columns = ['Team', 'Runs', 'Offensive_Adjustment',
                             'Runs_Allowed', 'Defensive_Adjustment']

    # calculate adjustments and add columns
    #cluster_final['Adjusted_Differential'] = cluster_final.Runs + cluster_final.Offensive_Adjustment + cluster_final.Defensive_Adjustment - cluster_final.Runs_Allowed
    cluster_final['Defensive_Adjustment'] = -cluster_final['Defensive_Adjustment']
    cluster_final['Adjusted_Runs_Scored'] = cluster_final.Runs + cluster_final.Offensive_Adjustment
    cluster_final['Adjusted_Runs_Allowed'] = cluster_final.Runs_Allowed + cluster_final.Defensive_Adjustment

    if file_name is not None:
        with open(file_name, 'w') as f:
            cluster_final.to_csv(f)

    return cluster_final





