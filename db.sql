
CREATE TABLE stock_price_daily(
    stock_daily_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    stock_name VARCHAR(10) NOT NULL,
    volume FLOAT NOT NULL,
    open_price FLOAT NOT NULL,
    high_price FLOAT NOT NULL,
    low_price FLOAT NOT NULL,
    exchange VARCHAR(15) NOT NULL,
    date_stamp DATE DEFAULT CURRENT_DATE
);

CREATE TABLE stock_price_current(
    stock_current_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    stock_name VARCHAR(10) NOT NULL,
    exchange VARCHAR(15) NOT NULL,
    current_price FLOAT NOT NULL,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
