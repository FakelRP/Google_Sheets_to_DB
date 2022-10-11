import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
from schedule import every, repeat, run_pending
import time


def get_usd_rate():  # Получение курса доллара с сайта ЦБ РФ
    url = 'https://www.cbr.ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    usd = soup.find_all('div', class_='col-md-2 col-xs-9 _right mono-num')
    str_usd = str(usd[1]).replace(',', '.')
    usd_float = float(str_usd[47:54])
    return usd_float


def google_sheet_to_df(spreadsheet_name, sheet_num):  # Получение данных из гугл таблицы и преобразование их в DataFrame
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials_path = 'credentials.json'
    credentials = sac.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(credentials)
    sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records()
    df = pd.DataFrame.from_dict(sheet)
    return df


@repeat(every(5).seconds)
def df_to_db():  # Добавление в DataFrame столбца 'стоимость в руб' и запись данных в БД
    engine = create_engine("postgresql://postgres:Petre535@127.0.0.1:5433/kanalservice")
    df = google_sheet_to_df('kanal_test', 0)
    usd_rate = get_usd_rate()  # Вызов функции для получения текущего курса
    price_rub = []  # Список для добавления данных из него в DataFrame
    for i in range(len(df)):  # Добавление в список
        df_price_usd = df.iloc[i]['стоимость_$']
        price_in_usd = "{:.2f}".format(df_price_usd * usd_rate)
        price_rub.append(price_in_usd)
    df.insert(loc=4, column='стоимость_руб', value=price_rub)
    print(df)
    df.to_sql('orders', engine, if_exists='replace', index=False)


if __name__ == '__main__':
    while True:
        run_pending()
        time.sleep(1)
