from war_functions.pecota_tables import *

pt = load_combined_pecota_table()

df = pd.read_csv('pecota_data/names.csv', index_col=0)
print(df.head())