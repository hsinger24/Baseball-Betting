import pandas as pd

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

def active_roster_adjustment(active_rosters, overall_war_predictions_preseason, frac_season = 0.0):
    # Active rosters comes from the get_all_active_roster function from get_active_roster in war_functions
    # overall_war_predictions_preseason comes from get_overall_war_predictions in war_functions
    # Instead of Fangraphs: https://www.baseballprospectus.com/leaderboards/pitching/

    active_roster_war_table = pd.DataFrame(columns = ['Team', 'WAR', 'WAR_proj'])
    fucked_name_list = []
    for team_dict in active_rosters:
        team_table = pd.DataFrame(columns = ['Name', 'WAR'])
        team = team_dict['team_name']
        roster = team_dict['team_roster']
        link = f'https://www.fangraphs.com/teams/{team.lower().replace(" ", "")}/depth-chart'
        fangraphs_table_hitters = pd.read_html(link)[-4][['Name', 'WAR']]
        fangraphs_table_pitchers = pd.read_html(link)[-1][['Name', 'WAR']]
        fangraphs_table = fangraphs_table_hitters.append(fangraphs_table_pitchers)
        for player, _ in roster:
            try:
                team_table = team_table.append(fangraphs_table[fangraphs_table.Name==player])
            except:
                fucked_name_list.append(player)
        active_roster_total_war = team_table.WAR.sum()
        war_proj = overall_war_predictions_preseason.loc[overall_war_predictions_preseason.team_name==team, 'projected_war'].values[0]
        team_series = pd.Series([team, active_roster_total_war, war_proj], index = active_roster_war_table.columns)
        active_roster_war_table = active_roster_war_table.append(team_series, ignore_index = True)
    return active_roster_war_table, fucked_name_list

                            




