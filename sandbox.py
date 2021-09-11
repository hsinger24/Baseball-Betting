import pandas as pd

results_tracker_base = pd.read_csv('results_tracker/results_tracker_base.csv')
results_tracker = results_tracker_base.iloc[:,7:]
results_tracker.to_csv('results_tracker/results_tracker_base.csv')