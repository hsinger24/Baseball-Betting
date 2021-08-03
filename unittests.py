import unittest
import os
import pandas as pd

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


# class TestActiveRosters(unittest.TestCase):
#     def test_retrieve_loads(self):
#         r1 = retrieve_all_active_rosters(None)

#         self.assertEqual(30, len(r1))

#     def test_retrieve_saves(self):
#         _ = retrieve_all_active_rosters(file_name="test_data/rosters.json")
#         self.assertTrue(os.path.exists("test_data/rosters.json"))
    
#     def test_load_data(self):
#         _ = retrieve_all_active_rosters(file_name="test_data/rosters.json")
#         l = load_active_rosters(file_name="test_data/rosters.json")
#         self.assertEqual(len(l), 30)

# class TestPecotaTables(unittest.TestCase):
#     def test_load_combined(self):
#         pt = load_combined_pecota_table()
#         self.assertEqual(len(pt), 8199)

# class TestWarTable(unittest.TestCase):
#     def test_retrieve(self):
#         r1 = retrieve_historical_combined_war_table(2020, file_path=None)

#         self.assertIsInstance(r1, pd.DataFrame)

#         self.assertEqual(r1[r1['Team'] == 'Dodgers']['Offense'].values[0], 12.4)
    
#     def test_load(self):
#         retrieve_historical_combined_war_table(2020, file_path="test_data/war_table_2020.csv")
#         wt = load_combined_war_table(file_path="test_data/war_table_2020.csv")
#         self.assertEqual(wt.shape, (30, 4))

# class TestWarPredictions(unittest.TestCase):
#     def test_calculate_team_war_projs(self):
#         retrieve_all_active_rosters(file_name="test_data/rosters.json")
#         rosters = load_active_rosters(file_name="test_data/rosters.json")
#         pecota = load_combined_pecota_table()

#         projections = calculate_team_war_projections_table(rosters, pecota)
#         self.assertEqual(projections.shape, (30, 2))


# class TestFinalWarTable(unittest.TestCase):
#     def test_calculate_final_war(self):
#         retrieve_all_active_rosters(file_name="test_data/rosters.json")
#         retrieve_historical_combined_war_table(2020, file_path="test_data/war_table_2020.csv")

#         rosters = load_active_rosters(file_name="test_data/rosters.json")
#         pecota = load_combined_pecota_table()
#         war_2020 = load_combined_war_table(file_path="test_data/war_table_2020.csv")

#         projections = calculate_team_war_projections_table(rosters, pecota)
#         final_war = calculate_final_war_table(projections, war_2020, 2021)

#         self.assertEqual(final_war.shape, (30, 4))
#         self.assertListEqual(final_war.columns.tolist(), ["Team", "2021", "2020", "Run_Change"])
    
class TestClusterLuckHitting(unittest.TestCase):
    def test_retrieve_historical_hitting_tables(self):
        ht = retrieve_historical_hitting_tables(2020, file_name=None)
        self.assertEqual(ht[ht['Team'] == 'Mets']['AB'].values[0] == 2023)

    def test_load_historical_hitting_tables(self):
        pass
    def test_calculate_regression_saves(self):
        pass
    def test_calculate_regression(self):
        pass
    def test_calculate_predicted_cluster_luck_adj(self):
        pass
        

def _clean_data():
    for root, dirs, files in os.walk("test_data"):
        for f in files:
            os.remove(root + "/" + f)

if __name__ == "__main__":
    _clean_data()
    unittest.main()