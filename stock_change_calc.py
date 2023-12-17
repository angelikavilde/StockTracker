"""File for calculating and tracking the stock price changes"""

from os import environ

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor


def get_db_conn() -> connection:
    """Retrieves database connection"""
    load_dotenv()
    return connect(environ["DB_IP"], cursor_factory=RealDictCursor)


def retrieve_all_stock_prices_recorded(conn: connection) -> list:
    """Returns all data from the table stock_price_current"""
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM stock_price_current""")
        data = cur.fetchall()
    conn.close()
    return data


def retrieve_all_stock_daily_price_changes(conn: connection) -> list:
    """Returns all data from the table stock_price_daily"""
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM stock_price_daily""")
        data = cur.fetchall()
    conn.close()
    return data


if __name__ == "__main__":
    db_conn = get_db_conn()
    print(retrieve_all_stock_prices_recorded(db_conn))
    print(retrieve_all_stock_daily_price_changes(db_conn))