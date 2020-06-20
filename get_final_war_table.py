import pandas as pd


def get_final_war_table(projected_war_table, previous_year_war_table):
    # merge tables to see WAR change from 2019 to 2020
    final_WAR_table = pd.merge(projected_war_table, previous_year_war_table,
                               left_on='team_name', right_on='Team')
    # adjust columns
    final_WAR_table.drop(['Team', 'Offense', 'Defense'], axis=1, inplace=True)
    final_WAR_table.columns = ['Team', '2020', '2019']

    # see run change between years
    final_WAR_table['Run_Change'] = (
        final_WAR_table['2020'] - final_WAR_table['2019']) * 10

    return final_WAR_table
