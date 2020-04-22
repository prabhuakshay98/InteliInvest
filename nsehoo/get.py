import requests
import datetime
from models import Stock, PriceHistory


def nse_date(date):
    months = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
              "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}
    day, month, year = date.split("-")
    month = months[month]
    return datetime.date(int(year), int(month), int(day))


def yahoo_date(date):
    year, month, day = date.split('-')
    return datetime.date(int(year), int(month), int(day))


def csv_to_list(resp):
    rows = resp.text.split('\n')
    cols = [x.split(',') for x in rows]
    return cols


def create_stock(lists, Stock=Stock):
    stocks = []
    for i in lists:
        stock = Stock(symbol=i[0], company_name=i[1], series=i[2],
                      listed_date=nse_date(i[3]), paidup_value=i[4], market_lot=i[5],
                      isin_number=i[6], face_val=i[7])
        stocks.append(stock)
    return stocks


def create_price(symbol, lists, PriceHistory=PriceHistory):
    prices = []
    for i in lists:
        price = PriceHistory(symbol=symbol, date=yahoo_date(i[0]), open_val=i[1],
                             high_val=i[2], low_val=i[3], close_val=i[4],
                             adj_val=i[5], volume=i[6])
        prices.append(price)
    return prices


def get_share_list():
    """
    Gets list of all listed shares on NSE. Downloadable in CSV format
    """
    url = "https://www1.nseindia.com/content/equities/EQUITY_L.csv"
    resp = requests.get(url)
    resp = csv_to_list(resp)[1:-1]
    return create_stock(resp)


def get_full_history(symbol):
    """
    Gets full data set for the given symbol
    """
    to_date = int(datetime.datetime.timestamp(datetime.datetime.now()))
    from_date = int(datetime.datetime.timestamp(datetime.datetime(1990, 1, 1, 1, 0, 0)))
    url_base = "https://query1.finance.yahoo.com/v7/finance/download/"
    url_params = f"{symbol}.NS?period1={from_date}&period2={to_date}&interval=1d&events=history"
    resp = requests.get(url_base + url_params)
    a = csv_to_list(resp)[1:]
    return create_price(symbol, a)


def add_to_db(objs, session):
    session.add_all(objs)
    session.commit()
    session.close()


if __name__ == "__main__":
    print(get_share_list())
