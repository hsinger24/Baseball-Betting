def sp_adjustment(games, starting_rotations, frac_season=0.0):

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

        home_table = starting_rotations[home_team]
        away_table = starting_rotations[away_team]

        home_pitch_war = (home_table.loc[home_table.Name==sp_home, 'WAR_proj'].values[0]*(1.0-frac_season)+home_table.loc[home_table.Name==sp_home, 'WAR'].values[0])*5.0
        home_team_war = home_table.WAR_proj.sum()*(1.0-frac_season)+home_table.WAR.sum()
        WAR_diff_home = home_pitch_war - home_team_war


        away_pitch_war = (away_table.loc[away_table.Name==sp_away, 'WAR_proj'].values[0]*(1.0-frac_season)+away_table.loc[away_table.Name==sp_away, 'WAR'].values[0])*5.0
        away_team_war = away_table.WAR_proj.sum()*(1.0-frac_season)+away_table.WAR.sum()
        WAR_diff_away = away_pitch_war - away_team_war

    

        game_dict = {'home_team': home_team, 'away_team': away_team, 'home_pitcher': sp_home, 'home_adjustment': WAR_diff_home, 'away_pitcher': sp_away,
            'away_adjustment': WAR_diff_away}

        sp_adjust_list.append(game_dict)
        
    return sp_adjust_list

