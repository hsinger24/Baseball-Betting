import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime as dt
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from war_functions.pecota_tables import *

from cluster_luck_functions.cluster_luck_hitting import *
from cluster_luck_functions.cluster_luck_pitching import *
from cluster_luck_functions.cluster_luck_combined import *

from daily_adjustments.active_rosters import *
from daily_adjustments.BP_WAR import *
from daily_adjustments.todays_game_info import *
from daily_adjustments.starting_rotations_WAR import *
from daily_adjustments.adjusted_war_today import *

from odds_and_other_projections import *

######### DELETING BETS ##########
bets_today = pd.read_csv('past_bets/base/bets_20210930.csv', index_col = 0)
bets_today.drop([10], axis = 0, inplace = True)
bets_today.reset_index(inplace = True, drop = True)
bets_today.to_csv('past_bets/base/bets_20210930.csv')

