import pandas as pd
import time
 

team_list = ['Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'Cubs', 'White Sox', 'Reds', 'Indians', 'Rockies',
                 'Tigers', 'Astros', 'Royals', 'Angels', 'Dodgers', 'Marlins', 'Brewers', 'Twins', 'Mets', 'Yankees',
                 'Athletics', 'Phillies', 'Pirates', 'Padres', 'Giants', 'Mariners', 'Cardinals', 'Rays', 'Rangers',
                 'Blue Jays', 'Nationals']

def get_starting_rotations_failed(pecota_table):
    pass
    # team_list_links = ['https://www.lineups.com/mlb/depth-charts/arizona-diamondbacks', 'https://www.lineups.com/mlb/depth-charts/atlanta-braves',
    #                    'https://www.lineups.com/mlb/depth-charts/baltimore-orioles', 'https://www.lineups.com/mlb/depth-charts/boston-red-sox',
    #                    'https://www.lineups.com/mlb/depth-charts/chicago-cubs', 'https://www.lineups.com/mlb/depth-charts/chicago-white-sox',
    #                    'https://www.lineups.com/mlb/depth-charts/cincinnati-reds', 'https://www.lineups.com/mlb/depth-charts/cleveland-indians',
    #                    'https://www.lineups.com/mlb/depth-charts/colorado-rockies', 'https://www.lineups.com/mlb/depth-charts/detroit-tigers',
    #                    'https://www.lineups.com/mlb/depth-charts/houston-astros', 'https://www.lineups.com/mlb/depth-charts/kansas-city-royals',
    #                    'https://www.lineups.com/mlb/depth-charts/los-angeles-angels', 'https://www.lineups.com/mlb/depth-charts/los-angeles-dodgers',
    #                    'https://www.lineups.com/mlb/depth-charts/miami-marlins', 'https://www.lineups.com/mlb/depth-charts/milwaukee-brewers',
    #                    'https://www.lineups.com/mlb/depth-charts/minnesota-twins', 'https://www.lineups.com/mlb/depth-charts/new-york-mets',
    #                    'https://www.lineups.com/mlb/depth-charts/new-york-yankees', 'https://www.lineups.com/mlb/depth-charts/oakland-athletics',
    #                    'https://www.lineups.com/mlb/depth-charts/philadelphia-phillies', 'https://www.lineups.com/mlb/depth-charts/pittsburgh-pirates',
    #                    'https://www.lineups.com/mlb/depth-charts/san-diego-padres', 'https://www.lineups.com/mlb/depth-charts/san-francisco-giants',
    #                    'https://www.lineups.com/mlb/depth-charts/seattle-mariners', 'https://www.lineups.com/mlb/depth-charts/st-louis-cardinals',
    #                    'https://www.lineups.com/mlb/depth-charts/tampa-bay-rays', 'https://www.lineups.com/mlb/depth-charts/texas-rangers',
    #                    'https://www.lineups.com/mlb/depth-charts/toronto-blue-jays', 'https://www.lineups.com/mlb/depth-charts/washington-nationals']

    # team_list = ['Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'Cubs', 'White Sox', 'Reds', 'Indians', 'Rockies',
    #              'Tigers', 'Astros', 'Royals', 'Angels', 'Dodgers', 'Marlins', 'Brewers', 'Twins', 'Mets', 'Yankees',
    #              'Athletics', 'Phillies', 'Pirates', 'Padres', 'Giants', 'Mariners', 'Cardinals', 'Rays', 'Rangers',
    #              'Blue Jays', 'Nationals']

    # # where every team's rotation will be stored
    # starting_rotations = {}

    # # iterate through all the links
    # for index, link in enumerate(team_list_links):

    #     # get the depth chart table related to starting pitching
    #     table = pd.read_html(link)[1]
    
    #     # cast column to a string
    #     table['Position'] = table['Position'].astype('string')
        
    #     # get only the starting rotation
    #     subset = table[table['Position'] == 'Rotation SP'].copy()

    #     # adjust columns
    #     subset.drop('Position', axis=1, inplace=True)
    #     subset.reset_index(inplace=True)
    #     subset.drop('index', axis=1, inplace=True)

    #     # more manipulating data to get the starting rotation
    #     sp_list = list(subset.iloc[0, :])
    #     sp = []
    #     for j in sp_list:
    #         #regex = r'^\S+\s\S+'
    #         regex = r'^.*? \S\.'
    #         pitch = re.search(regex, j)
    #         if pitch[0]:
    #             sp.append(pitch[0][:-3])
    #     starting_rotations.update({team_list[index]: sp})

    
    # # creating tables from the starting rotations
    # starting_rotations_tables = {}
    # failed_to_find_war_list = []
    # for index, team in enumerate(team_list):
    #     table = pd.DataFrame(columns=['Name', 'WAR'])
    #     for index2, pitcher in enumerate(starting_rotations[team]):
    #         table.loc[index2, 'Name'] = pitcher
    #         try:
    #             table.loc[index2, 'WAR'] = pecota_table[pecota_table['name'] == pitcher]['war_162'].iloc[0]
    #         except:
    #             try:
    #                 table.loc[index2, 'WAR'] = pecota_table[pecota_table['name_wo_a'] == pitcher]['war_162'].iloc[0]
    #             except:
    #                 table.loc[index2, 'WAR'] = 0
    #                 failed_to_find_war_list.append(pitcher)
    #     starting_rotations_tables[team] = table


    # return starting_rotations_tables, failed_to_find_war_list

def retrieve_starting_rotations_WAR(pecota_table, curr_year_WAR_BP):
    
    ##### Issue: Players just called up: for these players, use only Projected ##### 
    
    team_list = ['Diamondbacks', 'Braves', 'Orioles', 'Red Sox', 'Cubs', 'White Sox', 'Reds', 'Indians', 'Rockies',
                 'Tigers', 'Astros', 'Royals', 'Dodgers', 'Marlins', 'Brewers', 'Twins', 'Mets', 'Yankees',
                 'Athletics', 'Phillies', 'Pirates', 'Padres', 'Giants', 'Mariners', 'Cardinals', 'Rays', 'Rangers',
                 'Blue Jays', 'Nationals', 'Angels']
    names = pd.read_csv("pecota_data/names.csv", index_col=0)
    starting_rotations = {}
    failed_to_find_war_list = []
    for team in team_list:
        print(team)
        link = f'https://www.fangraphs.com/teams/{team.lower().replace(" ", "")}/depth-chart'
        try:
            dfs = pd.read_html(link)
        except:
            time.sleep(60)
            dfs = pd.read_html(link)
        starting_pitchers = dfs[-3]

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

        starting_rotations[team] = starting_pitchers
    return starting_rotations, failed_to_find_war_list
