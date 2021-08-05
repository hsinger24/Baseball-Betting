from player_adjustments.get_starting_rotations import *
from player_adjustments.get_todays_games_info import *
from player_adjustments.get_adjusted_war_table_for_today import *

from predictions.war_functions.active_rosters import *
from predictions.war_functions.final_war_table import *
from predictions.war_functions.war_projections_pecota import *
from predictions.war_functions.pecota_tables import *
from predictions.war_functions.historical_war_table import *

from predictions.cluster_luck_functions.get_cluster_luck_hitting import *
from predictions.cluster_luck_functions.get_cluster_luck_pitching import *
from predictions.cluster_luck_functions.get_combined_cluster_luck_table import *

from predictions.get_final_win_percentage_table import *

from external_work.odds_and_other_projections import *

from player_adjustments.getting_WAR_BP import *


#####Testing Player Adjustments Folder#####
curr_year_war_BP = load_current_year_WAR()
pt = load_combined_pecota_table()
st_rot, failed  = get_starting_rotations(pt, curr_year_war_BP)
print(st_rot)
print(failed)


# curr_year_war_BP = load_current_year_WAR()
# print(curr_year_war_BP[curr_year_war_BP.Name == 'Wily Peralta'])
# print(curr_year_war_BP)

######Testing War_Functions Folder######

# retrieve_all_active_rosters()
# active_rosters = load_active_rosters()
# pt = load_combined_pecota_table()
# projected_war_table = calculate_team_war_projections_table(active_rosters,pt)
# final = calculate_final_war_table(projected_war_table, load_previous_year_war_table(), 2021)

