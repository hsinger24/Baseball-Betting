import pandas as pd


def get_pecota_hitting_table():
    '''
    Gets the table for WAR predictions from Pecota
    Params:
        - None
    Returns:
        - A pandas dataframe holding all the hitting data
    '''
    # create the table from the file
    hitting_table = pd.read_csv('./predictions/pecota_data/pecota_hitting.csv')

    # adjust columns
    hitting_table.drop('pos', axis=1, inplace=True)
    hitting_table['war_162'] = (162/hitting_table['g'])*hitting_table['warp']

    # Changing players who have infinte WAR for 162 games
    for i in range(len(hitting_table.warp)):
        if hitting_table.loc[i, 'g'] == 0:
            hitting_table.loc[i, 'war_162'] = hitting_table.loc[i, 'warp']

    # don't need games column anymore
    hitting_table.drop('g', axis=1)

    return hitting_table


def get_pecota_pitching_table():
    '''
    Gets the table for WAR predictions from Pecota
    Params:
        - None
    Returns:
        - A pandas dataframe holding all the pitching data
    '''
    # create the table from the file
    pitching_table = pd.read_csv(
        './predictions/pecota_data/pecota_pitching.csv')

    # adjust columns
    pitching_table['g'] = 0
    pitching_table['war_162'] = pitching_table.warp

    # don't need games column anymore
    pitching_table.drop('g', axis=1)

    return pitching_table


def get_combined_pecota_table():
    table = pd.DataFrame.append(get_pecota_hitting_table(), get_pecota_pitching_table())
    table['name_wo_a'] = table.first_name + ' ' + table.last_name
    return table

