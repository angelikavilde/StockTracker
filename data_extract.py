"""Extract file for API requests for stock data"""

from os import environ

from dotenv import load_dotenv
from requests import get, ConnectionError, Timeout
from psycopg2 import DatabaseError
from psycopg2.extensions import connection

from stock_change_calc import get_db_conn


def get_api_token() -> str:
    """Retrieves token environment value"""
    load_dotenv()
    return environ.get('API_TOKEN')


def add_stock_current_price(conn: connection, stock_data) -> None:
    """Adds the stock to the database for current prices recorded"""
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO stock_price_current(stock_name, current_price) VALUES (%s, %s)""",
                    [i for i in stock_data.items()][0] )
        data = cur.fetchall()
    return data


def get_stock_data(api_token, stock_list: list) -> None:
    """Retrieves the data on the current stock price for each stock"""
    for stock in stock_list:
        try:
            response = get(f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api_token}", verify=False, timeout=60)
        except Timeout as e:
            print("API request has timed-out: ", e)
        except ConnectionError as e:
            print("Connection error from API request: ", e)
            # ! Add logics to make it loop back in this case
        # TODO use this API endpoint for daily data rather than current
        data = response.json()
        stock_data = {stock : data['c']}
        add_stock_current_price(stock_data)


def retrieve_all_tracked_stocks(conn: connection) -> list:
    """Retrieves a list of all stocks that are tracked from the database"""
    with conn.cursor() as cur:
        cur.execute("""SELECT distinct stock_name FROM stock_price_daily""")
        data = cur.fetchall()
    return data


if __name__ == "__main__":
    api_token = get_api_token()
    try:
        db_connection = get_db_conn()
        all_stocks_tracked = retrieve_all_tracked_stocks(db_connection)
        all_stocks_tracked = ["AAPL"]
        get_stock_data(api_token, all_stocks_tracked)
        db_connection.close()
    except DatabaseError as e:
        print("Error connecting to database: ", e)