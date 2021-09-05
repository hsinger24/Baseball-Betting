from odds_and_other_projections import *
import pandas as pd

retrieve_external_data()
data = load_external_data()
capital_athletic = 100000
capital_538 = 100000
capital_combined = 100000

def kc(row, kelly, Athletic, Home):
    if (Athletic) & (Home):
        diff = row.Home_Prob_Athletic - row.Home_Prob_Implied
        if diff<0:
            return 0
        else:
            p = row.Home_Prob_Athletic
            q = 1-p
            ml = row.Home_ML
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
    if (Athletic) & (not Home):
        diff = row.Away_Prob_Athletic - row.Away_Prob_Implied
        if diff<0:
            return 0
        else:
            p = row.Away_Prob_Athletic
            q = 1-p
            ml = row.Away_ML
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
    if (not Athletic) & (Home):
        diff = row.Home_Prob_538 - row.Home_Prob_Implied
        if diff<0:
            return 0
        else:
            p = row.Home_Prob_538
            q = 1-p
            ml = row.Home_ML
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
    if (not Athletic) & (not Home):
        diff = row.Away_Prob_538 - row.Away_Prob_Implied
        if diff<0:
            return 0
        else:
            p = row.Away_Prob_538
            q = 1-p
            ml = row.Away_ML
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

data['Home_KC_Athletic'] = data.apply(kc, axis = 1, kelly = 10, Athletic = True, Home = True)
data['Away_KC_Athletic'] = data.apply(kc, axis = 1, kelly = 10, Athletic = True, Home = False)
data['Home_KC_538'] = data.apply(kc, axis = 1, kelly = 10, Athletic = False, Home = True)
data['Away_KC_538'] = data.apply(kc, axis = 1, kelly = 10, Athletic = False, Home = False)
data['Home_Combined'] = data.apply(lambda x: (x.Home_KC_Athletic+x.Home_KC_538)/2 if (x.Home_KC_Athletic>0) &
    (x.Home_KC_538>0) else 0, axis = 1)
data['Away_Combined'] = data.apply(lambda x: (x.Away_KC_Athletic+x.Away_KC_538)/2 if (x.Away_KC_Athletic>0) &
    (x.Away_KC_538>0) else 0, axis = 1)
data['Bet_Athletic'] = data.apply(lambda x: capital_athletic * x.Home_KC_Athletic if x.Home_KC_Athletic>0
    else capital_athletic * x.Away_KC_Athletic, axis = 1)
data['Bet_538'] = data.apply(lambda x: capital_538 * x.Home_KC_538 if x.Home_KC_538>0
    else capital_538 * x.Away_KC_538, axis = 1)
data['Bet_Combined'] = data.apply(lambda x: capital_combined * x.Home_Combined if x.Home_Combined>0
    else capital_combined * x.Away_Combined, axis = 1)
data.to_csv('data/test.csv')