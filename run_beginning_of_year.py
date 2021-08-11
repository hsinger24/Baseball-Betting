from cluster_luck_functions.cluster_luck_hitting import *
from cluster_luck_functions.cluster_luck_pitching import *
from cluster_luck_functions.cluster_luck_combined import *

########## Cluster Luck ##########



##### Getting cluster luck hitting #####

retrieve_historical_hitting_tables([2019, 2018, 2017])
historical_hitting_table = load_historical_hitting_tables()
calculate_and_save_hitting_linear_regression(historical_hitting_table)
hitting_reg = load_linear_regression("data/hitting_regression.pickle")
prev_year_hitting_table = retrieve_historical_hitting_tables(2019)
prev_year_hitting_adjustment = calculate_predicted_cluster_luck_run_adjustment_hitting(hitting_reg, prev_year_hitting_table)

##### Getting cluster luck pitching #####

retrieve_historical_pitching_tables([2019, 2018, 2017])
historical_pitching_table = load_historical_pitching_tables()
calculate_and_save_pitching_linear_regression(historical_pitching_table)
pitching_reg = load_linear_regression('./data/pitching_regression.pickle')
prev_year_pitching_table = retrieve_historical_pitching_tables(2019)
prev_year_pitching_adjustment = calculate_predicted_cluster_luck_run_adjustment_pitching(pitching_reg, prev_year_pitching_table)

##### Merging #####

final_cluster_luck = merge_cluster_luck_tables(prev_year_hitting_adjustment, prev_year_pitching_adjustment)
print(final_cluster_luck.head())
