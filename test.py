from player_adjustments.get_starting_rotations import *
from player_adjustments.get_todays_games_info import *
from player_adjustments.get_adjusted_war_table_for_today import *

from predictions.war_functions.active_rosters import *
from predictions.war_functions.final_war_table import *
from predictions.war_functions.war_projections import *
from predictions.war_functions.pecota_tables import *
from predictions.war_functions.war_table import *

from predictions.cluster_luck_functions.get_cluster_luck_hitting import *
from predictions.cluster_luck_functions.get_cluster_luck_pitching import *
from predictions.cluster_luck_functions.get_combined_cluster_luck_table import *

from predictions.get_final_win_percentage_table import *

from external_work.odds_and_other_projections import *


retrieve_all_active_rosters()
retrieve_historical_combined_war_table(2020)

war_2020 = load_combined_war_table()
pecota = load_combined_pecota_table()
rosters = load_active_rosters()

war_projections = calculate_team_war_projections_table(rosters, pecota)
final_table = calculate_final_war_table(war_projections, war_2020, 2021)

print(final_table)






