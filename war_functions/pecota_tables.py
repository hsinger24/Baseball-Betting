import pandas as pd

def _load_pecota_hitting_table(file_name='pecota_data/pecota_hitting.csv'):
    '''
    Gets the table for WAR predictions from Pecota. Should not be used outsid this file
    Params:
        - file_name (str, optional): the file_name to read the pecota table
    Returns:
        - A pandas dataframe holding all the hitting data
    '''
    # create the table from the file
    hitting_table = pd.read_csv(file_name)

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

def _load_pecota_pitching_table(file_name='pecota_data/pecota_pitching.csv'):
    '''
    Gets the table for WAR predictions from Pecota
    Params:
        - file_name (str, optional): The file name to read the data from
    Returns:
        - A pandas dataframe holding all the pitching data
    '''
    # create the table from the file
    pitching_table = pd.read_csv(file_name)

    # adjust columns
    pitching_table['g'] = 0
    pitching_table['war_162'] = pitching_table.warp

    # don't need games column anymore
    pitching_table.drop('g', axis=1)

    return pitching_table

def load_combined_pecota_table(data_path=None):
    """Loads both PECOTA hitting and pitching and returns a combined dataframe
    Params:
        data_path (str, optional): if data_path is not None, then it is the path to the PECOTA tables
        otherwise the default path is `./pecota_data`
    Returns:
        pandas.DataFrame: Combined hitting and pitching PECOTA Tables
    """
    # Load hitting and pitching tables from file
    if data_path is None:
        ht = _load_pecota_hitting_table()
        pt = _load_pecota_pitching_table()
    else:
        ht = _load_pecota_hitting_table(data_path + "/pecota_hitting.csv")
        pt = _load_pecota_pitching_table(data_path + "/pecota_pitching.csv")
    
    # Create new DataFrame
    table = pd.DataFrame.append(ht, pt)

    # Create new Column for name without accents
    table['name_wo_a'] = table.first_name + ' ' + table.last_name
    return table

