import pandas as pd


########## DELETING BETS ##########
bets_today = pd.read_csv('past_bets/base/bets_20210922.csv', index_col = 0)
bets_today.drop([1,], axis = 0, inplace = True)
bets_today.reset_index(inplace = True, drop = True)
bets_today.to_csv('past_bets/base/bets_20210922.csv')
