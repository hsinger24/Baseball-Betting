from odds_and_other_projections import *
import pandas as pd

retrieve_external_data()
data = load_external_data()
print(data.columns)

def kc(row, kelly, Athletic, Home):
    if Athletic & Home:
        diff = row.Home_Prob_Athletic
        if diff<0:
            return 0
        else:
            p = row.Home_Prob_Athletic
            q = 1-p
            ml = home_ml
            if ml>=0:
                b = (ml/100)
            if ml<0:
                b = (100/abs(ml))
            kc = ((p*b) - q) / b
            if (kc > 0.5) & (kc<0.6):
                return kc/(kelly+2)
            if (kc > 0.6) & (kc<0.7):
                return kc/(kelly+4)
            if kc > 0.7:
                return kc/(kelly+7)
            else:
                return kc/kelly
