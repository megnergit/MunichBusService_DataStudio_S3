
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from pathlib import Path
import os
import pandas as pd
import config
# Read parameters from `config.py`. `config.py` is NOT in GitHub repo.
# ====================================================================
SPREADSHEET_KEY = config.SPREADSHEET_KEY
DATA_DIR = config.DATA_DIR

mbs_pn = 'mbs_pn.csv'
mbs_ds = 'mbs_ds.csv'  # store for data studio
df = pd.read_csv(DATA_DIR/mbs_pn, parse_dates=['created_at_tz'])

df['is_Positive'] = [1 if p == 1 else 0 for p in df['sentiment_digit']]
df['is_Negative'] = [1 if p == -1 else 0 for p in df['sentiment_digit']]
df['is_Neutral'] = [1 if p == 0 else 0 for p in df['sentiment_digit']]

df.to_csv(DATA_DIR/mbs_ds, index=False)
# ====================================================================
scope = 'https://spreadsheets.google.com/feeds'
credentials_file_path = './client_secret.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    credentials_file_path, scope)

gc = gspread.authorize(credentials)
workbook = gc.open_by_key(SPREADSHEET_KEY)

update_files = ['mbs_ds', 'mbs_geo']
for f in update_files:
    workbook.values_update(f,  # name of sheet
                           params={'valueInputOption': 'USER_ENTERED'},
                           body={'values': list(csv.reader(
                               open(DATA_DIR/(f+'.csv'))))
                           }
                           )
