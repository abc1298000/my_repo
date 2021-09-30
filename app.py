import anvil.server
import numpy as np
import pandas as pd
import pickle
from urllib.request import urlopen

link = urlopen(r"https://github.com/abc1298000/my_repo/raw/eed8bcf0268ee7d2f6c9de87efe317bf8c5eccb6/pipeline.pkl")
data_pipeline = pickle.load(link)

cols = ['age_logarithmic', 'education_rank', 'hours_per_week', 'marital_status',\
    'sex', 'gain/loss', 'Local_gov', 'Private', 'Self_emp_inc',\
    'Self_emp_not_in_inc', 'State_gov', 'others', 'Asian_Pac_Islander',\
    'Black', 'Other', 'White', 'Armed_Forces', 'Craft_repair',\
    'Exec_managerial', 'Farming_fishing', 'Handlers_cleaners',\
    'Machine_op_inspct', 'Other_service', 'Priv_house_serv',\
    'Prof_specialty', 'Protective_serv', 'Sales', 'Tech_support',\
    'Transport_moving', 'El Salvador', 'Germany', 'India', 'Mexico',\
    'Philippines', 'Puerto Rico', 'United States', 'others']


dct = {'10th': 6.0,'11th': 7.0,'12th': 8.0,'1st-4th': 2.0,'5th-6th': 3.0,'7th-8th': 4.0,\
'9th': 5.0,'Assoc-acdm': 12.0, 'Assoc-voc': 11.0,\
'Bachelors': 13.0, 'Doctorate': 16.0,'HS-grad': 9.0, 'Masters': 14.0,'Preschool': 1.0,\
    'Prof-school': 15.0,'Some-college': 10.0}


anvil.server.connect("UWAXNIPZNKJ7SFTIJ7DRTWXP-XEZ5Q6KTQRZIXOLS")

@anvil.server.callable
def predict(age, education, hours_per_week, marital_status, sex, gain_or_loss, workclass, race, occupation, country):
    x = np.zeros(37)
    x[0] = age
    x[1] = dct[education]
    x[2] = hours_per_week
    x[3] = marital_status
    if sex == 'Male':
      x[4] = 1
    else:
      x[4] = 0
    x[5] = gain_or_loss
    if workclass in cols[:12]:
      x[cols[:12].index(workclass)] = 1
    if race == 'others':
      x[14] = 1
    elif race == 'Asian_Pac_Islander':
      x[cols.index('Asian_Pac_Islander')] = 1
    elif race == 'Black':
      x[cols.index('Black')] = 1
    elif race == 'White':
      x[cols.index('White')] = 1
    if occupation in cols:
      x[cols.index(occupation)] = 1
    if country == 'others':
      x[36] = 1
    elif country in cols:
      x[cols.index(country)] = 1


    test_row = pd.DataFrame(x).transpose()
    test_row.columns = cols
    result = data_pipeline.predict(test_row)

    return result[0]
anvil.server.wait_forever()