import pandas as pd
import datetime as dt


def merge_cluster_luck_tables(hitting_table, pitching_table):
    last_year = dt.date.today().year - 1 
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
    
    if last_year == 2020:
        cluster_final['Adjusted_Runs_Scored'] = cluster_final.Runs*162/60.0 + cluster_final.Offensive_Adjustment
        cluster_final['Adjusted_Runs_Allowed'] = cluster_final.Runs_Allowed*162/60.0 + cluster_final.Defensive_Adjustment
    else:
        cluster_final['Adjusted_Runs_Scored'] = cluster_final.Runs + cluster_final.Offensive_Adjustment
        cluster_final['Adjusted_Runs_Allowed'] = cluster_final.Runs_Allowed + cluster_final.Defensive_Adjustment

    return cluster_final





