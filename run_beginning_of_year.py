import datetime as dt

from daily_adjustments.active_rosters import *
from daily_adjustments.BP_WAR import *

from cluster_luck_functions.cluster_luck_hitting import *
from cluster_luck_functions.cluster_luck_pitching import *
from cluster_luck_functions.cluster_luck_combined import *

from war_functions.pecota_tables import *
#from war_functions.historical_war_table import *
from war_functions.preseason_war_projections import *
from war_functions.preseason_win_percentage import *

current_year = dt.date.today().year

# ########## ACTIVE ROSTER BEGINNING OF YEAR ##########

retrieve_all_active_rosters()
rosters = load_active_rosters()

# ########## CLUSTER LUCK ##########

# # Getting cluster luck hitting #

retrieve_historical_hitting_tables([2021, 2019, 2018, 2017])
historical_hitting_table = load_historical_hitting_tables()
calculate_and_save_hitting_linear_regression(historical_hitting_table)
hitting_reg = load_linear_regression("data/hitting_regression.pickle")
prev_year_hitting_table = retrieve_historical_hitting_tables(2021, file_name = None)
prev_year_hitting_adjustment = calculate_predicted_cluster_luck_run_adjustment_hitting(hitting_reg, prev_year_hitting_table)

# # Getting cluster luck pitching #

retrieve_historical_pitching_tables([2021, 2019, 2018, 2017])
historical_pitching_table = load_historical_pitching_tables()
calculate_and_save_pitching_linear_regression(historical_pitching_table)
pitching_reg = load_linear_regression('./data/pitching_regression.pickle')
prev_year_pitching_table = retrieve_historical_pitching_tables(2021, file_name = None)
prev_year_pitching_adjustment = calculate_predicted_cluster_luck_run_adjustment_pitching(pitching_reg, prev_year_pitching_table)

# # Merging #

final_cluster_luck = merge_cluster_luck_tables(prev_year_hitting_adjustment, prev_year_pitching_adjustment, file_name = 'data/final_cluster_luck.csv')

########## WAR FUNCTIONS ##########

pt = load_combined_pecota_table()
retrieve_previous_year_war_table(2022)
prev_year_war = load_previous_year_war_table()
preseason_projections = calculate_preaseason_war_projections(rosters, pt)
final_war_preseason = calculate_final_preseason_war_change(preseason_projections, prev_year_war, current_year = current_year, file_name = 'data/overall_war_predictions_preseason.csv')
final_preseason_win_percentage = calculate_preseason_win_percentage(final_cluster_luck, final_war_preseason, current_year, file_name = 'data/preseason_projections.csv')


