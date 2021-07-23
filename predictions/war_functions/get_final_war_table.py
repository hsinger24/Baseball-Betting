import pandas as pd
import datetime as dt


def get_final_war_table(projected_war_table, previous_year_war_table):
    current_year = dt.date.today().year
    # merge tables to see WAR change from 2019 to 2020
    final_WAR_table = pd.merge(projected_war_table, previous_year_war_table,
                               left_on='team_name', right_on='Team')
    # adjust columns
    final_WAR_table.drop(['Team', 'Offense', 'Defense'], axis=1, inplace=True)
    final_WAR_table.columns = ['Team', str(current_year), str(current_year-1)]

    # see run change between years
    if current_year == 2021:
        final_WAR_table[str(current_year-1)] = final_WAR_table[str(current_year-1)]*(162.0/60.0)
        final_WAR_table['Run_Change'] = (
            final_WAR_table[str(current_year)] - final_WAR_table[str(current_year-1)]) * 10
    else: 
        final_WAR_table['Run_Change'] = (
            final_WAR_table[str(current_year)] - final_WAR_table[str(current_year-1)]) * 10

    return final_WAR_table
