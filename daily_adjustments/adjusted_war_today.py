import pandas as pd
import unidecode

def calculate_sp_adjustment(games, starting_rotations, pt, frac_season=0.0):
    """Calculates the starting pitcher adjustment for each team

    Args:
        games = output of retrieve_todays_game_info()
        starting_rotations = output of retrieve_starting_rotations_war
        pt = output of load_combined_pecota_table
        frac_season = fraction of the season expressed as a decimal

    Returns:
        (list of dicts): a list of dicts, one dict for each team + roster
    """

    # Getting starting pitcher names, and each teams' rotation
    names = pd.read_csv("pecota_data/names.csv", index_col=0)
    sp_adjust_list = []
    for game in games:
        sp_home = game['home_team']['starting_pitcher']
        home_team = game['home_team']['team_name']
        sp_away = game['away_team']['starting_pitcher']
        away_team = game['away_team']['team_name']
        if home_team == 'D-backs':
            home_team = 'Diamondbacks'
        if away_team == 'D-backs':
            away_team = 'Diamondbacks'  
        if (sp_home == 'TBD' or sp_away == 'TBD'):
            continue 

        # Getting starting rotation WAR tables for home and away team and adjusting data for players not found
        home_table = starting_rotations[home_team]
        for index, row in home_table.iterrows():
            if row.WAR==0.0001:
                home_table.loc[index, 'WAR']==row.WAR_proj
            if row.WAR_proj==0.001:
                home_table.loc[index, 'WAR_proj']==row.WAR
        away_table = starting_rotations[away_team]
        for index, row in away_table.iterrows():
            if row.WAR==0.0001:
                away_table.loc[index, 'WAR']==row.WAR_proj
            if row.WAR_proj==0.001:
                away_table.loc[index, 'WAR_proj']==row.WAR

        # Getting possibility of names for both home and away pitcher
        sp_home_short = sp_home
        sp_away_short = sp_away
        for col in names.columns:
                if sp_home in names[col].values:
                    sp_home = names[names[col]==sp_home]
                    break
        if type(sp_home) == str:
                print(sp_home, home_team)
        for col in names.columns:
                if sp_away in names[col].values:
                    sp_away = names[names[col]==sp_away]
                    break
        if type(sp_away) == str:
                print(sp_away, home_team)

        # Getting WAR difference for home team
        try:
            home_pitch_war = (home_table.loc[home_table.Name==sp_home['name'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+home_table.loc[home_table.Name==sp_home['name'].values[0], 'WAR'].values[0])*5.0
            gs_home = home_table.loc[home_table.Name==sp_home['name'].values[0], 'GS_P'].values[0]
        except:
            try:
                home_pitch_war = (home_table.loc[home_table.Name==sp_home['name_wo_a'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+home_table.loc[home_table.Name==sp_home['name_wo_a'].values[0], 'WAR'].values[0])*5.0
                gs_home = home_table.loc[home_table.Name==sp_home['name_wo_a'].values[0], 'GS_P'].values[0]
            except:
                try:
                    home_pitch_war = (home_table.loc[home_table.Name==sp_home['name_alt_1'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+home_table.loc[home_table.Name==sp_home['name_alt_1'].values[0], 'WAR'].values[0])*5.0
                    gs_home = home_table.loc[home_table.Name==sp_home['name_alt_1'].values[0], 'GS_P'].values[0]
                except:
                    try:
                        home_pitch_war = (home_table.loc[home_table.Name==sp_home['name_alt_2'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+home_table.loc[home_table.Name==sp_home['name_alt_2'].values[0], 'WAR'].values[0])*5.0
                        gs_home = home_table.loc[home_table.Name==sp_home['name_alt_2'].values[0], 'GS_P'].values[0]
                    except:
                        try:
                            home_pitch_war = (home_table.loc[home_table.Name==sp_home['name_alt_3'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+home_table.loc[home_table.Name==sp_home['name_alt_3'].values[0], 'WAR'].values[0])*5.0
                            gs_home = home_table.loc[home_table.Name==sp_home['name_alt_3'].values[0], 'GS_P'].values[0]
                        except:
                            try:
                                home_pitch_war = (home_table.loc[home_table.Name==sp_home['name_alt_4'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+home_table.loc[home_table.Name==sp_home['name_alt_4'].values[0], 'WAR'].values[0])*5.0
                                gs_home = home_table.loc[home_table.Name==sp_home['name_alt_4'].values[0], 'GS_P'].values[0]
                            except:
                                try:
                                    home_pitch_war = pt[pt['name'] == sp_home['name'].values[0]]['war_162'].iloc[0]
                                    gs_home = 0
                                    print('All names failed for', sp_home, 'Pecota WAR is:', home_pitch_war)
                                except:
                                    home_pitch_war = 0
                                    gs_home = 0
                                    print('All name failed for', sp_home, 'Do not bet on this game')

        # Accounting for injured players/players called up
        try:
            if (frac_season>=0.25) & (frac_season < 0.5) & (gs_home<=2):
                home_pitch_war = pt[pt['name'] == sp_home['name'].values[0]]['war_162'].iloc[0]
                print(sp_home, 'Was injured/called up recently')
            if (frac_season>=0.5) & (frac_season < 0.75) & (gs_home<=3):
                home_pitch_war = pt[pt['name'] == sp_home['name'].values[0]]['war_162'].iloc[0]
                print(sp_home, 'Was injured/called up recently')
            if (frac_season>0.75) & (gs_home<=4):
                home_pitch_war = pt[pt['name'] == sp_home['name'].values[0]]['war_162'].iloc[0]
                print(sp_home, 'Was injured/called up recently')
        except:
            home_pitch_war = 0
            print(sp_home , 'Do not bet on this game')
        
        # Adjusting rotation table to only consider pitchers with significant # of starts
        if (frac_season>=0.25) & (frac_season < 0.5):
            home_table = home_table[home_table.GS_P>2] 
        if (frac_season>=0.5) & (frac_season < 0.75):
            home_table = home_table[home_table.GS_P>3]
        if (frac_season>0.75):
            home_table = home_table[home_table.GS_P>5]
        
        # Calculating pitcher WAR difference based on fraction of season
        if frac_season>0.25:
            home_team_war = home_table.WAR_proj.sum()*(1.0-frac_season)+home_table.WAR.sum()
        else:
            home_team_war = home_table.WAR_proj.sum()
        WAR_diff_home = home_pitch_war - home_team_war


        # Getting WAR difference for away team
        try:
            away_pitch_war = (away_table.loc[away_table.Name==sp_away['name'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+away_table.loc[away_table.Name==sp_away['name'].values[0], 'WAR'].values[0])*5.0
            gs_away = away_table.loc[away_table.Name==sp_away['name'].values[0], 'GS_P'].values[0]
        except:
            try:
                away_pitch_war = (away_table.loc[away_table.Name==sp_away['name_wo_a'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+away_table.loc[away_table.Name==sp_away['name_wo_a'].values[0], 'WAR'].values[0])*5.0
                gs_away = away_table.loc[away_table.Name==sp_away['name_wo_a'].values[0], 'GS_P'].values[0]
            except:
                try:
                    away_pitch_war = (away_table.loc[away_table.Name==sp_away['name_alt_1'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+away_table.loc[away_table.Name==sp_away['name_alt_1'].values[0], 'WAR'].values[0])*5.0
                    gs_away = away_table.loc[away_table.Name==sp_away['name_alt_1'].values[0], 'GS_P'].values[0]
                except:
                    try:
                        away_pitch_war = (away_table.loc[away_table.Name==sp_away['name_alt_2'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+away_table.loc[away_table.Name==sp_away['name_alt_2'].values[0], 'WAR'].values[0])*5.0
                        gs_away = away_table.loc[away_table.Name==sp_away['name_alt_2'].values[0], 'GS_P'].values[0]
                    except:
                        try:
                            away_pitch_war = (away_table.loc[away_table.Name==sp_away['name_alt_3'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+away_table.loc[away_table.Name==sp_away['name_alt_3'].values[0], 'WAR'].values[0])*5.0
                            gs_away = away_table.loc[away_table.Name==sp_away['name_alt_3'].values[0], 'GS_P'].values[0]
                        except:
                            try:
                                away_pitch_war = (away_table.loc[away_table.Name==sp_away['name_alt_4'].values[0], 'WAR_proj'].values[0]*(1.0-frac_season)+away_table.loc[away_table.Name==sp_away['name_alt_4'].values[0], 'WAR'].values[0])*5.0
                                gs_away = away_table.loc[away_table.Name==sp_away['name_alt_4'].values[0], 'GS_P'].values[0]
                            except:
                                try:
                                    away_pitch_war = pt[pt['name'] == sp_away['name'].values[0]]['war_162'].iloc[0]
                                    gs_away = 0
                                    print('All names failed for', sp_away, 'Pecota WAR is:', away_pitch_war)
                                except:
                                    away_pitch_war = 0
                                    gs_away = 0
                                    print('All name failed for', sp_away, 'Do not bet on this game')

         # Accounting for injured players/players called up
        try:
            if (frac_season>=0.25) & (frac_season < 0.5) & (gs_away<=2):
                away_pitch_war = pt[pt['name'] == sp_away['name'].values[0]]['war_162'].iloc[0]
                print(sp_away, 'Was injured/called up recently')
            if (frac_season>=0.5) & (frac_season < 0.75) & (gs_away<=3):
                away_pitch_war = pt[pt['name'] == sp_away['name'].values[0]]['war_162'].iloc[0]
                print(sp_away, 'Was injured/called up recently')
            if (frac_season>0.75) & (gs_away<=4):
                away_pitch_war = pt[pt['name'] == sp_away['name'].values[0]]['war_162'].iloc[0]
                print(sp_away, 'Was injured/called up recently')
        except:
            away_pitch_war = 0
            print(sp_away , 'Do not bet on this game')

        # Adjusting rotation table to only consider pitchers with significant # of starts
        if (frac_season>=0.25) & (frac_season < 0.5):
            away_table = away_table[away_table.GS_P>2] 
        if (frac_season>=0.5) & (frac_season < 0.75):
            away_table = away_table[away_table.GS_P>3]
        if (frac_season>0.75):
            away_table = away_table[away_table.GS_P>5]
        
        # Calculating pitcher WAR difference based on fraction of season
        if (frac_season>0.25):
            away_team_war = away_table.WAR_proj.sum()*(1.0-frac_season)+away_table.WAR.sum()
        else:
            away_team_war = away_table.WAR_proj.sum()
        WAR_diff_away = away_pitch_war - away_team_war

        # Appending dictionary of result to list of games
        game_dict = {'home_team': home_team, 'away_team': away_team, 'home_pitcher': sp_home_short, 'home_adjustment': WAR_diff_home, 'away_pitcher': sp_away_short,
            'away_adjustment': WAR_diff_away}
        sp_adjust_list.append(game_dict)
        
    return sp_adjust_list

def calculate_active_roster_war_table(active_rosters, overall_war_predictions_preseason, curr_year_WAR_BP, pecota_table, current_year, frac_season = 0.0):
    """Calculates the active roster adjustment for each team

    Args:
        active_rosters = output of retrieve_all_active_rosters
        overall_war_predictions_preseason = pd.read_csv('data/overall_war_predictions_preseason.csv')
        curr_year_WAR_BP = output of retrieve_current_year_WAR/load_current_year_WAR
        pecota_table = output of load_combined_pecota_table
        current_year = current_year
        frac_season = fraction of the season expressed as a decimal

    Returns:
        (list of dicts): a list of dicts, one dict for each team + roster
    """

    # Instantiating stuff
    names = pd.read_csv("pecota_data/names.csv", index_col=0)
    active_roster_war_table = pd.DataFrame(columns = ['Team', 'active_roster_WAR', 'preseason_WAR_proj'])
    failed_to_find_players = []
    
    # Iteration through for each team
    for team_dict in active_rosters:
        team_table = pd.DataFrame(columns = ['Name', 'WAR', 'WAR_Proj'])
        team = team_dict['team_name']
        roster = team_dict['team_roster']
        
        # Iterating through for each player
        for player_name, _ in roster:
            for col in names.columns:
                if player_name in names[col].values:
                    player = names[names[col]==player_name]
                    break
            
            # Getting current year WAR and games played for each player
            position = None
            try:
                current_year_war = curr_year_WAR_BP[curr_year_WAR_BP.Name == player['name'].values[0]].iloc[0,1]
                if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name'].values[0], 'Position'].values[0] == 'P':
                    position = 'P'
                    gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name'].values[0]].iloc[0,2]
                if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name'].values[0], 'Position'].values[0] == 'H':
                    position = 'H'
                    gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name'].values[0]].iloc[0,3]
            except:
                try:
                    current_year_war = curr_year_WAR_BP[curr_year_WAR_BP.Name == player['name_wo_a'].values[0]].iloc[0,1]
                    if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_wo_a'].values[0], 'Position'].values[0] == 'P':
                        position = 'P'
                        gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_wo_a'].values[0]].iloc[0,2]
                    if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_wo_a'].values[0], 'Position'].values[0] == 'H':
                        position = 'H'
                        gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_wo_a'].values[0]].iloc[0,3]
                except:
                    try:
                        current_year_war = curr_year_WAR_BP[curr_year_WAR_BP.Name == player['name_alt_1'].values[0]].iloc[0,1]
                        if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_alt_1'].values[0], 'Position'].values[0] == 'P':
                            position = 'P'
                            gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_alt_1'].values[0]].iloc[0,2]
                        if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_alt_1'].values[0], 'Position'].values[0] == 'H':
                            position = 'H'
                            gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_alt_1'].values[0]].iloc[0,3]
                    except:
                        try:
                            current_year_war = curr_year_WAR_BP[curr_year_WAR_BP.Name == player['name_alt_2'].values[0]].iloc[0,1]
                            if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_alt_2'].values[0], 'Position'].values[0] == 'P':
                                position = 'P'
                                gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_alt_2'].values[0]].iloc[0,2]
                            if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_alt_2'].values[0], 'Position'].values[0] == 'H':
                                position = 'H'
                                gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_alt_2'].values[0]].iloc[0,3]
                        except:
                            try:
                                current_year_war = curr_year_WAR_BP[curr_year_WAR_BP.Name == player['name_alt_3'].values[0]].iloc[0,1]
                                if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_alt_3'].values[0], 'Position'].values[0] == 'P':
                                    position = 'P'
                                    gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_alt_3'].values[0]].iloc[0,2]
                                if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_alt_3'].values[0], 'Position'].values[0] == 'H':
                                    position = 'H'
                                    gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_alt_3'].values[0]].iloc[0,3]
                            except:
                                try:
                                    current_year_war = curr_year_WAR_BP[curr_year_WAR_BP.Name == player['name_alt_4'].values[0]].iloc[0,1]
                                    if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_alt_4'].values[0], 'Position'].values[0] == 'P':
                                        position = 'P'
                                        gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_alt_4'].values[0]].iloc[0,2]
                                    if curr_year_WAR_BP.loc[curr_year_WAR_BP.Name == player['name_alt_4'].values[0], 'Position'].values[0] == 'H':
                                        position = 'H'
                                        gs = curr_year_WAR_BP[curr_year_WAR_BP.Name==player['name_alt_4'].values[0]].iloc[0,3]
                                except:
                                    failed_to_find_players.append(player_name + 'BP')
                                    current_year_war = 0
                                    gs = 0

            # Adjusting WAR for injured players/players recently called up
            if position is not None:
                try:
                    if position == 'H':
                        if (frac_season>=0.25) & (frac_season<0.5) & (gs<10):
                            current_year_war = pecota_table[pecota_table['name'] == player['name'].values[0]]['war_162'].iloc[0]
                        if (frac_season>=0.50) & (frac_season<0.75) & (gs<20):
                            current_year_war = pecota_table[pecota_table['name'] == player['name'].values[0]]['war_162'].iloc[0]
                        if (frac_season>=0.75) & (gs<30):
                            current_year_war = pecota_table[pecota_table['name'] == player['name'].values[0]]['war_162'].iloc[0]
                except:
                    current_year_war = 0
                try:
                    if position == 'P':
                        if (frac_season>=0.25) & (frac_season<0.5) & (gs<2):
                            current_year_war = pecota_table[pecota_table['name'] == player['name'].values[0]]['war_162'].iloc[0]
                        if (frac_season>=0.50) & (frac_season<0.75) & (gs<3):
                            current_year_war = pecota_table[pecota_table['name'] == player['name'].values[0]]['war_162'].iloc[0]
                        if (frac_season>=0.75) & (gs<4):
                            current_year_war = pecota_table[pecota_table['name'] == player['name'].values[0]]['war_162'].iloc[0]
                except:
                    current_year_war = 0
            if position is None:
                current_year_war = 0
            
            # Getting projected WAR for player
            try:
                projected_war = pecota_table[pecota_table['name'] == player['name'].values[0]]['war_162'].iloc[0]
            except:
                try:
                    projected_war = pecota_table[pecota_table['name'] == player['name_wo_a'].values[0]]['war_162'].iloc[0]
                except:
                    try:
                        projected_war = pecota_table[pecota_table['name'] == player['name_alt_1'].values[0]]['war_162'].iloc[0]
                    except:
                        try:
                            projected_war = pecota_table[pecota_table['name'] == player['name_alt_2'].values[0]]['war_162'].iloc[0]
                        except:
                            try:
                                projected_war = pecota_table[pecota_table['name'] == player['name_alt_3'].values[0]]['war_162'].iloc[0]
                            except:
                                try:
                                    projected_war = pecota_table[pecota_table['name'] == player['name_alt_4'].values[0]]['war_162'].iloc[0]
                                except:
                                    failed_to_find_players.append(player_name + 'Pecota')
                                    projected_war = 0
            
            # Appending player's data
            player_series = pd.Series([player_name, current_year_war, projected_war], index = team_table.columns)
            team_table = team_table.append(player_series, ignore_index = True)
        
        # Finding team's total WAR based on fraction of season
        active_roster_total_war_current = team_table.WAR.sum()
        active_roster_total_war_proj = team_table.WAR_Proj.sum()
        if frac_season>0.25:
            active_roster_war = active_roster_total_war_proj*(1.0-frac_season) + active_roster_total_war_current
        else:
            active_roster_war = active_roster_total_war_proj
        preseason_war_proj = overall_war_predictions_preseason.loc[overall_war_predictions_preseason.Team==team, str(current_year)].values[0]
        team_series = pd.Series([team, active_roster_war, preseason_war_proj], index = active_roster_war_table.columns)
        active_roster_war_table = active_roster_war_table.append(team_series, ignore_index = True)
    
    # Appending team's total WAR
    active_roster_war_table['WAR_difference'] = active_roster_war_table.active_roster_WAR - active_roster_war_table.preseason_WAR_proj
    active_roster_war_table['Run_difference'] = active_roster_war_table['WAR_difference']*10
    return active_roster_war_table, failed_to_find_players

                            




