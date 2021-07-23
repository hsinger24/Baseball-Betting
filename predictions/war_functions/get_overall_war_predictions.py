import pandas as pd


def get_overall_war_predictions(active_rosters, pecota_table):
    # adding active players to each team to only count their war
    #   and not the inactive players
    teams_active_players_war = {}
    for team in active_rosters:
        team_data_frame = pd.DataFrame(columns=pecota_table.columns)
        for player in team['team_roster']:
            player_column = pecota_table[pecota_table.mlbid == int(player[1])]

            # TODO Shohei can start as both a hitter or pitcher
            # Handles duplicate players assuming they are a batter
            if player_column.shape[0] > 1:
                player_column = player_column.iloc[0,:]
            team_data_frame = pd.DataFrame.append(
                team_data_frame, player_column)
        teams_active_players_war[team['team_name']] = team_data_frame
        
      
    # setting up final team war table
    overall_war_predictions_table = pd.DataFrame(
        columns=['team_name', 'projected_war'])

    # summing active players wars for team total
    i = 0
    for key, value in teams_active_players_war.items():
        overall_war_predictions_table.loc[i] = [key, value['war_162'].sum()]
        i += 1

    return overall_war_predictions_table
