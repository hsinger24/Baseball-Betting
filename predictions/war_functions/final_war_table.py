import pandas as pd

def calculate_final_war_table(projected_war_table, previous_year_war_table, current_year):
    """A function that produces a DataFrame with current year's war (projected),
    last year's war actual, and the corresponding run difference 

    Args:
        projected_war_table (pandas.DataFrame): The result of calculate_war_projections_table(...)
        previous_year_war_table (pandas.DataFrame): The result of load_combined_war_table()
        current_year (int): the current year

    Returns:
        pandas.DataFrame: A dataframe with team projected wars, previous wars and the difference
    """
    # Merge tables to see WAR change from last year to projected (this) year on the Team name
    final_WAR_table = pd.merge(projected_war_table, previous_year_war_table, left_on='team_name', right_on='Team')
    
    # Adjust columns so remaining columns are [Team, war_162 (projections from Pecota), Total (Actual from prev year)]
    final_WAR_table.drop(['Team'], axis=1, inplace=True)
    final_WAR_table.columns = ['Team', str(current_year), str(current_year-1)]

    # see run change between years
    # Corner Case for 2021 since 2020 had 60 games
    if current_year == 2021:
        final_WAR_table[str(current_year-1)] = final_WAR_table[str(current_year-1)]*(162.0/60.0)
        
        # Formula Converting WAR difference to Runs
        final_WAR_table['Run_Change'] = (
            final_WAR_table[str(current_year)] - final_WAR_table[str(current_year-1)]) * 10
    else:
        # Formula Converting WAR difference to Runs
        final_WAR_table['Run_Change'] = (
            final_WAR_table[str(current_year)] - final_WAR_table[str(current_year-1)]) * 10

    return final_WAR_table
