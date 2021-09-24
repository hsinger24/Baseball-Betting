import pandas as pd
from daily_adjustments.BP_WAR import *
from daily_adjustments.starting_rotations_WAR import *
from war_functions.pecota_tables import *

######### DELETING BETS ##########
bets_today = pd.read_csv('past_bets/base/bets_20210924.csv', index_col = 0)
bets_today.drop([9], axis = 0, inplace = True)
bets_today.reset_index(inplace = True, drop = True)
bets_today.to_csv('past_bets/base/bets_20210924.csv')


