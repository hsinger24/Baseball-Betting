import pandas as pd
import time
import ssl
 

team_list = ['Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'Cubs', 'White Sox', 'Reds', 'Guardians', 'Rockies',
                 'Tigers', 'Astros', 'Royals', 'Angels', 'Dodgers', 'Marlins', 'Brewers', 'Twins', 'Mets', 'Yankees',
                 'Athletics', 'Phillies', 'Pirates', 'Padres', 'Giants', 'Mariners', 'Cardinals', 'Rays', 'Rangers',
                 'Blue Jays', 'Nationals']


def retrieve_starting_rotations_WAR(pecota_table, curr_year_WAR_BP):
    
    ##### Issue: Players just called up: for these players, use only Projected ##### 
    
    ssl._create_default_https_context = ssl._create_unverified_context
    team_list = ['Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'Cubs', 'White Sox', 'Reds', 'Guardians', 'Rockies',
                 'Tigers', 'Astros', 'Royals', 'Marlins', 'Brewers', 'Twins', 'Mets', 'Yankees',
                 'Athletics', 'Phillies', 'Pirates', 'Padres', 'Giants', 'Mariners', 'Cardinals', 'Rays', 'Rangers',
                 'Blue Jays', 'Nationals', 'Angels', 'Dodgers',]
    names = pd.read_csv("pecota_data/names.csv", index_col=0)
    starting_rotations = {}
    failed_to_find_war_list = []
    curr_year_GS = curr_year_WAR_BP[['Name', 'GS_P']]
    for team in team_list:
        if team != 'Dodgers':
            link = f'https://www.fangraphs.com/teams/{team.lower().replace(" ", "")}/depth-chart'
            dfs = pd.read_html(link)
            starting_pitchers = dfs[-3]
        else:
            link = 'https://www.fangraphs.com/depthcharts.aspx?position=ALL&teamid=22'
            dfs = pd.read_html(link)
            starting_pitchers = dfs[-4]
        starting_pitchers['Name'] = starting_pitchers[['Name']]
        starting_pitchers = starting_pitchers.loc[starting_pitchers['Name'] != 'Total']
        starting_pitchers['WAR_proj'] = 0
        starting_pitchers['WAR'] = 0
        sp_list = starting_pitchers[['Name']].values
        for index, pitcher in enumerate(sp_list):
            pitcher = pitcher[0] 

            # Getting row of potential names from names df
            
            for col in names.columns:
                if pitcher in names[col].values:
                    pitcher = names[names[col]==pitcher]
                    break
            
            if type(pitcher) == str:
                failed_to_find_war_list.append(pitcher + ' Pecota')
                continue
            # Getting projected WAR from Pecota table

            try:
                starting_pitchers.loc[index, 'WAR_proj'] = pecota_table[pecota_table['name'] == pitcher['name'].values[0]]['war_162'].iloc[0]
            except:
                starting_pitchers.loc[index, 'WAR_proj'] = 0.0001
                failed_to_find_war_list.append(pitcher['names_wo_a'].values[0] + ' Pecota')
            
            # Getting current WAR from BP
            try:
                starting_pitchers.loc[index, 'WAR'] = curr_year_WAR_BP[curr_year_WAR_BP.Name==pitcher['name'].values[0]].iloc[0,1]
            except:
                try:
                    starting_pitchers.loc[index, 'WAR'] = curr_year_WAR_BP[curr_year_WAR_BP.Name==pitcher['name_wo_a'].values[0]].iloc[0,1]
                except:
                    try:
                        starting_pitchers.loc[index, 'WAR'] = curr_year_WAR_BP[curr_year_WAR_BP.Name==pitcher['name_alt_1'].values[0]].iloc[0,1]
                    except:
                        try:
                            starting_pitchers.loc[index, 'WAR'] = curr_year_WAR_BP[curr_year_WAR_BP.Name==pitcher['name_alt_2'].values[0]].iloc[0,1]
                        except:
                            try:
                                starting_pitchers.loc[index, 'WAR'] = curr_year_WAR_BP[curr_year_WAR_BP.Name==pitcher['name_alt_3'].values[0]].iloc[0,1]
                            except:
                                try:
                                    starting_pitchers.loc[index, 'WAR'] = curr_year_WAR_BP[curr_year_WAR_BP.Name==pitcher['name_alt_4'].values[0]].iloc[0,1]
                                except:
                                    failed_to_find_war_list.append(pitcher['name_wo_a'].values[0] + ' BP')
                                    starting_pitchers.loc[index, 'WAR'] = 0.0001
        starting_pitchers = pd.merge(starting_pitchers, curr_year_GS, on = 'Name', how = 'left')
        starting_pitchers.fillna(0, inplace = True)

        # Corner cases
        if team == 'Blue Jays':
            starting_pitchers.loc[starting_pitchers.Name=='Hyun-Jin Ryu', 'GS_P'] = 20
        if team == 'Cardinals':
            starting_pitchers.loc[starting_pitchers.Name=='Kwang-hyun Kim', 'GS_P'] = 20
        if team == 'Dodgers':
            starting_pitchers.loc[starting_pitchers.Name=='Julio UrÃ­as', 'GS_P'] = 20

        starting_rotations[team] = starting_pitchers
    return starting_rotations, failed_to_find_war_list
