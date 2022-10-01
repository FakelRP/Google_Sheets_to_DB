import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd
import sqlalchemy as sa


def gsheet2df(spreadsheet_name, sheet_num):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials_path = 'credentials.json'

    credentials = sac.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(credentials)

    sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records()
    df = pd.DataFrame.from_dict(sheet)

    print(df)

    return df.head()

gsheet2df('kanal_test', 0)
