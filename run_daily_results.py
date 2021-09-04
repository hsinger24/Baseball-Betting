import pandas as pd
import datetime as dt

today = dt.date.today()
yesterday = today - dt.timedelta(days=1)
yesterday = str(yesterday)
yesterday = yesterday.replace('-', '')
link = 'https://www.espn.com/mlb/scoreboard/_/date/' + yesterday