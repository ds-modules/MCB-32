from datascience import *
from gspread_pandas.spread import Spread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate to Google
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ['GOOGLE_SHEETS_READONLY_KEY']), scope)

def get_spreadsheet(url, sheet_name):
    spread = Spread(url, creds=creds)
    sheet_df = spread.sheet_to_df(sheet=sheet_name, index=None)
    return Table.from_df(sheet_df)
