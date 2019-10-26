import sqlite3
import csv


def refresh_data():
    conn = sqlite3.connect('stocks.db')    
    c = conn.cursor()
    with conn:
        c.execute("DROP TABLE IF EXISTS stock_data")
        c.execute("CREATE TABLE IF NOT EXISTS stock_data (stocktype text, stockdate text, open_price integer, high_price integer, low_price integer, close_price integer, last_closing_price integer, percent_change integer)")
        print('Table created successfully..!!!')

def load_data():
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    with open('stockdata.csv') as f:
        csvreader = csv.DictReader(f)
        with conn:
            for row in csvreader:
                c.execute("INSERT INTO stock_data values(:stocktype, :stockdate, :open_price, :high_price, :low_price, :close_price, :last_closing_price, :percent_change)", row)
    print('Data Loaded successfully...!!')

refresh_data()
load_data()
