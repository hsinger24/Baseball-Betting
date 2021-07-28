from player_adjustments.get_starting_rotations import *
from player_adjustments.get_todays_games_info import *
from player_adjustments.get_adjusted_war_table_for_today import *

from predictions.war_functions.get_active_roster import *
from predictions.war_functions.get_final_war_table import *
from predictions.war_functions.get_overall_war_predictions import *
from predictions.war_functions.get_pecota_tables import *
from predictions.war_functions.get_previous_year_war import *

from predictions.cluster_luck_functions.get_cluster_luck_hitting import *
from predictions.cluster_luck_functions.get_cluster_luck_pitching import *
from predictions.cluster_luck_functions.get_combined_cluster_luck_table import *

from predictions.get_final_win_percentage_table import *

pt = get_combined_pecota_table()
r = get_all_active_rosters()
op = get_overall_war_predictions(r, pt)

table,fucked = active_roster_adjustment(r, op)

print(fucked)




