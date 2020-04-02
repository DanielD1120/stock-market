import pymysql
from flask import Flask, jsonify, request, Response
import time
import sys

app = Flask(__name__)
db = None

def connect_to_database():
    global db

    # Open database connection
    while True:
        try:
            db = pymysql.connect(host = "mysql-dev", user = "root", password = "password", db = "stocks")
            break
        except:
            continue

@app.route('/login', methods=['GET'])
def login():
    args = request.args
    user = args.get('username')
    passwd = args.get('password')

    connect_to_database()
    cursor = db.cursor()

    try:
        cursor.execute("select * from admin_credentials where username = \"" + user + "\" and pass = \"" \
            + passwd + "\"")
    except pymysql.err.MySQLError as e:
        return "Error at login!\n" + str(e)

    rows = cursor.fetchall()
    cursor.close()
    db.close()

    if len(rows) == 0:
        return "Login failed!"
    else:
        return "Login succesfull!"

@app.route('/get_stocks', methods=['GET'])
def get_bought():
    connect_to_database()
    cursor = db.cursor()
    stocks_string = '{:15}'.format('Name') + '{:15}'.format('Buy Price') + '{:15}'.format('Sell Price') + '\n'
    cursor.execute("select * from stocks_table")
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    for row in rows:
        stocks_string += '{:15}'.format(str(row[1])) + '{:15}'.format( str(row[2]) + "$") \
            + '{:15}'.format(str(row[3]) + "$") + '\n'

    return stocks_string[:-1]

@app.route('/add_stock', methods=['PUT'])
def add_stock():
    args = request.args
    stock_name = args.get('stock_name')
    buy_price = args.get('buy_price')
    sell_price = args.get('sell_price')
    qty = args.get('qty')
    connect_to_database()
    values_to_add = "(\"{}\", {}, {}, {})".format(stock_name,
                                              buy_price,
                                              sell_price,
                                              qty)
    cursor = db.cursor()

    try:
        cursor.execute("insert into stocks_table(stock_name, buy_price, sell_price, qty) values " + values_to_add)
    except pymysql.err.MySQLError as e:
        return "Error inserting stock!\n" + str(e)

    db.commit()
    cursor.close()
    db.close()

    return "Stock for {} succesfully added!".format(stock_name)

@app.route('/update_stock', methods=['PUT'])
def update_stock():
    args = request.args
    stock_name = args.get('stock_name')
    buy_price = args.get('buy_price')
    sell_price = args.get('sell_price')
    connect_to_database()
    cursor = db.cursor()

    try:
        cursor.execute("update stocks_table set buy_price = " + str(buy_price) + ", sell_price" \
            "= " + str(sell_price) + " where stock_name = " + "\'" + str(stock_name) + "\'" )
    except pymysql.err.MySQLError as e:
        return "Error updating stock!\n" + str(e)

    db.commit()
    cursor.close()
    db.close()

    return "Stock for {} succesfully updated!".format(stock_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
