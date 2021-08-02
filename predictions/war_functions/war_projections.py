import pandas as pd

def calculate_team_war_projections_table(active_rosters, pecota_table):
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

    return overall_war_predictions_table
