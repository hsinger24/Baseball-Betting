from player_adjustments.get_starting_rotations import *
from player_adjustments.get_todays_games_info import *
from player_adjustments.get_adjusted_war_table_for_todays_pitchers import *

from predictions.war_functions.get_active_roster import *
from predictions.war_functions.get_final_war_table import *
from predictions.war_functions.get_overall_war_predictions import *
from predictions.war_functions.get_pecota_tables import *
from predictions.war_functions.get_previous_year_war import *

from predictions.cluster_luck_functions.get_cluster_luck_hitting import *
from predictions.cluster_luck_functions.get_cluster_luck_pitching import *
from predictions.cluster_luck_functions.get_combined_cluster_luck_table import *

from predictions.get_final_win_percentage_table import *

ht = get_cluster_luck_hitting_table()
pt = get_cluster_luck_hitting_table()
cl = get_combined_cluster_luck_table(ht, pt)



# games = get_todays_games_info()
# pt = get_combined_pecota_table()
# starting_rotations, f = get_starting_rotations(pt)
# print(sp_adjustment(games, starting_rotations, 0.500))
# hey this is a comment I did stuff