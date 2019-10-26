import sqlite3
from datetime import datetime as dt


# helper method to add column names in output result dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# This function returns net value changed data for given stock type from specific date
# The result will be array of objects and each object has x value as unix timestamp and y value as amount
# The amount is derived based on initial value 100000

def getNetPrice(stocktype, stockdate):
    conn = sqlite3.connect('stocks.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    result = {}
    output = []
    amt = 100000

    # selecting the data based on stocktype and stockdate
    with conn:
        c.execute("SELECT * FROM stock_data WHERE stockdate >= ? and stocktype = ?", (stockdate, stocktype))

    # looping through all records and calculate the amount relative to the initial amount 
    for r in c.fetchall():
        temp = {}
        temp['x'] = int(dt.strptime(r['stockdate'],'%Y%m%d').timestamp()*1000)
        amt = amt + (amt * r['percent_change'])
        temp['y'] = round(amt)
        output.append(temp)
    result['type'] = stocktype
    result['data'] = output
    return result


# This function returns stock data for the combination of stock and bond ratio from specific date
# The result will be array of objects and each object has x value as unix timestamp and y value as amount
# The amount is derived based on initial value 100000

def getPerformance(stockdate, stock_percent, bond_percent):
    amt = 100000
    SP = stock_percent/100
    BP = bond_percent/100
    result = {}
    output = []
    title = f"{stock_percent}% Stock and {bond_percent}% Bond"

    conn = sqlite3.connect('stocks.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    
    with conn:
        c.execute("SELECT stockdate, max(CASE WHEN stocktype = 'VTSMX' THEN percent_change END) AS SPC, max(CASE WHEN stocktype = 'VBMFX' THEN percent_change END) AS BPC FROM stock_data WHERE stockdate >= ? group by stockdate ORDER BY stockdate",(stockdate,))
    
    for r in c.fetchall():
        temp = {}
        temp['x'] = int(dt.strptime(r['stockdate'],'%Y%m%d').timestamp()*1000)
        diff = amt*SP*r['SPC'] + amt*BP*r['BPC']
        amt += diff
        temp['y'] = round(amt)
        output.append(temp)
    
    result['title'] = title
    result['data'] = output
    return result