import pandas as pd
import pickle
import datetime as dt

def calculate_preaseason_war_projections(active_rosters, pecota_table, file_name = None):
    """Given Active Rosters and a Pecota Table, this function returns a DataFrame of the
    projected WARs of each team

    Args:
        active_rosters (list of dicts): The result of load_active_rosters()
        pecota_table (pandas.DataFrame): The result of load_combined_pecota_table() 

    Returns:
        pandas.DataFrame: DataFrame of predicted Team WARs
    """
    # adding active players to each team to only count their war
    #   and not the inactive players
    teams_active_players_war = {}

    # For every Team
    for team in active_rosters:
        # Create a DataFrame for a Team
        team_data_frame = pd.DataFrame(columns=pecota_table.columns)
        # For every player in the roster
        for player in team['team_roster']:
            # Get their row from the PECOTA
            player_row = pecota_table[pecota_table.mlbid == int(player[1])]

            # TODO Shohei can start as both a hitter or pitcher

            # Handles duplicate players assuming they are a batter
            if player_row.shape[0] > 1:
                player_row = player_row.iloc[0,:]
            # Append the Player's Row to the Team DataFrame
            team_data_frame = pd.DataFrame.append(team_data_frame, player_row)
        # Add the Team DF to the dict of DFs
        teams_active_players_war[team['team_name']] = team_data_frame
        
    
    # TODO Delete v for loop and include logic in ^ for loop

    # setting up final team war table
    overall_war_predictions_table = pd.DataFrame(columns=['team_name', 'projected_war'])

    # summing active players wars for team total
    i = 0
    for key, value in teams_active_players_war.items():
        overall_war_predictions_table.loc[i] = [key, value['war_162'].sum()]
        i += 1

    if file_name is not None:
        overall_war_predictions_table.to_csv(file_name)

    return overall_war_predictions_table

def calculate_final_preseason_war_change(pecota_projected_war_table, previous_year_war_table, current_year, file_name = None):
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
    final_WAR_table = pd.merge(pecota_projected_war_table, previous_year_war_table, left_on='team_name', right_on='Team')
    
    # Adjust columns so remaining columns are [Team, war_162 (projections from Pecota), Total (Actual from prev year)]
    final_WAR_table.drop(['Team'], axis=1, inplace=True)
    final_WAR_table.columns = ['Team', str(current_year), str(current_year-1)]

        # Formula Converting WAR difference to Runs
    final_WAR_table['Run_Change'] = (
        final_WAR_table[str(current_year)] - final_WAR_table[str(current_year-1)]) * 10

    if file_name is not None:
        final_WAR_table.to_csv(file_name)

    return final_WAR_table

def calculate_win_percentage_predictions(cluster_luck_table, final_preseason_war_projections, file_name=False):
    """A function that produces a DataFrame with each team's projected win percentage for the upcoming year

    Args:
        cluster_luck_table: The result of merge_cluster_luck_tables()
        final_preseason_war_projections: 
        file_name: Place to save the file. Defaults to none

    Returns:
        DF with final preseason win % projections
    """
    
    current_year = dt.date.today().year
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