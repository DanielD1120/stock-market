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
        cursor.execute("select * from users_table where username = \"" + user + "\" and pass = \"" \
            + passwd + "\"")
    except pymysql.err.MySQLError as e:
        return "Error at login!\n" + str(e)

    rows = cursor.fetchall()
    cursor.close()
    db.close()

    if len(rows) == 0:
        return "Login failed!"
    else:
        return "Login succesfull, welcome " + str(rows[0][1]) + "!"

@app.route('/create_acc', methods=['GET'])
def create_acc():
    args = request.args
    user = args.get('username')
    passwd = args.get('password')

    values_to_add = "(\"{}\", \"{}\", 0)".format(user,
                                                passwd)

    connect_to_database()
    cursor = db.cursor()

    try:
        cursor.execute("insert into users_table(username, pass, balance) values " + values_to_add)
    except pymysql.err.MySQLError as e:
        return "Error creating acc!\n" + str(e)

    db.commit()
    cursor.close()
    db.close()

    return "Account created successfully!"

@app.route('/info', methods=['GET'])
def info():
    args = request.args
    user = args.get('username')
    return_str = ""

    connect_to_database()
    cursor = db.cursor()

    try:
        cursor.execute("select * from users_table where username = \"" + user + "\"")
    except pymysql.err.MySQLError as e:
        return "Error getting info!\n" + str(e)

    rows = cursor.fetchall()
    cursor.close()
    db.close()

    return_str += "User: " + str(rows[0][1]) + "\t\tBalance: " + str(rows[0][3]) + "$"

    return return_str

@app.route('/add_money', methods=['GET'])
def add_money():
    args = request.args
    user = args.get('username')
    money = args.get('money')

    connect_to_database()
    cursor = db.cursor()

    try:
        cursor.execute("update users_table set balance = balance + " + money  + " where username = \"" + user + "\"")
    except pymysql.err.MySQLError as e:
        return "Error adding money!\n" + str(e)

    db.commit()
    cursor.close()
    db.close()

    return "Deposit successfull"

@app.route('/sell_stock', methods=['GET'])
def sell_stock():
    args = request.args
    user = args.get('username')
    stock_name = args.get('stock_name')
    qty = args.get('quantity')

    connect_to_database()
    cursor = db.cursor()

    # get sell price and stock id

    try:
        cursor.execute("select * from stocks_table where stock_name = \"" + stock_name + "\"")
    except pymysql.err.MySQLError as e:
        return "Error getting price and stock id!\n" + str(e)

    rows = cursor.fetchall()

    sell_price = float(rows[0][3])
    stock_id = int(rows[0][0])

    print(str(sell_price) + " " + str(stock_id), flush=True)

    # get user id

    try:
        cursor.execute("select id from users_table where username = \"" + user + "\"")
    except pymysql.err.MySQLError as e:
        return "Error getting user id!\n" + str(e)

    rows = cursor.fetchall()

    user_id = rows[0][0]

    print(str(user_id), flush=True)


    # check for qty

    try:
        cursor.execute("select qty from users_stocks where stock_id = " + str(stock_id) + \
            " and user_id = " + str(user_id))
    except pymysql.err.MySQLError as e:
        return "Error getting qty!\n" + str(e)

    rows = cursor.fetchall()

    if len(rows) == 0:
        return "Sell failed! You do not have this stock!"

    current_qty = int(rows[0][0])
    qty = int(qty)

    print(str(qty) + " " + str(current_qty), flush=True)

    if qty > current_qty:
        return "Sell failed! You do not have that many stocks!"

    # make the sell

    # delete stocks from user
    if qty == current_qty:
        try:
            cursor.execute("delete from users_stocks where stock_id = " + str(stock_id) + \
                " and user_id = " + str(user_id))
        except pymysql.err.MySQLError as e:
            return "Error deleting stocks from user!\n" + str(e)
    else:
        new_qty = current_qty - qty
        try:
            cursor.execute("update users_stocks set qty = " + str(new_qty)  + " where user_id = " + str(user_id) \
                 + " and stock_id = " + str(stock_id))
        except pymysql.err.MySQLError as e:
            return "Error deleting stocks from user!\n" + str(e)

    print("Sell made", flush=True)

    # update global qty
    try:
        cursor.execute("update stocks_table set qty = qty + " + str(qty)  + " where id = " + str(stock_id))
    except pymysql.err.MySQLError as e:
        return "Error updating global qty!\n" + str(e)

    #add to balance

    money_to_add = qty * sell_price

    try:
        cursor.execute("update users_table set balance = balance + " + str(money_to_add)  + " where username = \"" + user + "\"")
    except pymysql.err.MySQLError as e:
        return "Error adding to balance!\n" + str(e)

    print("Money added to balance", flush=True)

    db.commit()
    cursor.close()
    db.close()

    return "Sell successfull"

@app.route('/buy_stock', methods=['GET'])
def buy_stock():
    args = request.args
    user = args.get('username')
    stock_name = args.get('stock_name')
    qty = int(args.get('quantity'))

    connect_to_database()
    cursor = db.cursor()

    # get buy price and stock id and disponible qty

    try:
        cursor.execute("select * from stocks_table where stock_name = \"" + stock_name + "\"")
    except pymysql.err.MySQLError as e:
        return "Error getting buy price and stock id!\n" + str(e)

    rows = cursor.fetchall()

    buy_price = float(rows[0][2])
    stock_id = int(rows[0][0])
    current_qty = int(rows[0][4])

    print(str(buy_price) + " " + str(stock_id), flush=True)

    # get user id and balance

    try:
        cursor.execute("select * from users_table where username = \"" + user + "\"")
    except pymysql.err.MySQLError as e:
        return "Error getting user id and balance!\n" + str(e)

    rows = cursor.fetchall()

    user_id = rows[0][0]
    balance = float(rows[0][3])

    print(str(user_id), flush=True)

    # check if the qty is available

    if qty > current_qty:
        return "Buy failed! Not enough stocks are available!"

    # check if you have enough money

    total_price = buy_price * qty

    if balance < total_price:
        return "Buy failed! Not enough money!"

    # make the buy

    # delete stocks from stock_table
    new_qty = current_qty - qty
    try:
        cursor.execute("update stocks_table set qty = " + str(new_qty)  + " where id = " + str(stock_id))
    except pymysql.err.MySQLError as e:
        return "Error deleting stocks from stock table!\n" + str(e)

    print("Buy made", flush=True)

    # insert into users_stocks

    try:
        cursor.execute("select * from users_stocks where user_id = " + str(user_id) \
                 + " and stock_id = " + str(stock_id))
    except pymysql.err.MySQLError as e:
        return "Error at select from user_stocks!\n" + str(e)

    rows = cursor.fetchall()

    qty_to_add = qty
    new_price = buy_price

    if len(rows) != 0:
        qty_to_add = int(rows[0][3] + qty)
        new_price = (qty * buy_price + int(rows[0][3]) * float(rows[0][2])) / qty_to_add
        try:
            cursor.execute("delete from users_stocks where user_id = " + str(user_id) \
                    + " and stock_id = " + str(stock_id))
        except pymysql.err.MySQLError as e:
            return "Error at delete from user_stocks!\n" + str(e)

    try:
        cursor.execute("insert into users_stocks values (" + str(user_id) + "," + str(stock_id) \
            + "," + str(new_price) + "," + str(qty_to_add) + ")")
    except pymysql.err.MySQLError as e:
        return "Error at insert into user_stocks!\n" + str(e)

    #remove from balance

    remaining_money = balance - total_price

    try:
        cursor.execute("update users_table set balance = " + str(remaining_money)  + " where username = \"" + user + "\"")
    except pymysql.err.MySQLError as e:
        return "Error at updating users balance!\n" + str(e)

    print("Money removed from balance", flush=True)

    db.commit()
    cursor.close()
    db.close()

    return "Buy successfull"

@app.route('/get_my_stocks', methods=['GET'])
def get_my_stocks():
    args = request.args
    user = args.get('username')

    connect_to_database()
    cursor = db.cursor()

    try:
        cursor.execute("select * from users_stocks a join users_table b on a.user_id = b.id join stocks_table c on a.stock_id = c.id where username = \"" + user + "\"")
    except pymysql.err.MySQLError as e:
        return "Error getting user stocks!\n" + str(e)

    rows = cursor.fetchall()
    cursor.close()
    db.close()

    stocks_string = '{:15}'.format('Name') + '{:15}'.format('Buy Price') + '{:15}'.format('Sell Price') \
        + '{:15}'.format('My Price') + '{:15}'.format('Quantity') + '\n'
    for row in rows:
        stocks_string += '{:15}'.format(str(row[9])) + '{:15}'.format( str(row[10]) + "$") \
            + '{:15}'.format(str(row[11]) + "$") + '{:15}'.format(str(row[2]) + "$") + '{:15}'.format(str(row[3])) + '\n'

    return stocks_string


@app.route('/get_stocks', methods=['GET'])
def get_bought():
    connect_to_database()
    cursor = db.cursor()
    stocks_string = '{:15}'.format('Name') + '{:15}'.format('Buy Price') + '{:15}'.format('Sell Price') + '{:15}'.format('Quantity') + '\n'
    try:
        cursor.execute("select * from stocks_table")
    except pymysql.err.MySQLError as e:
        return "Error getting all stocks!\n" + str(e)
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    for row in rows:
        stocks_string += '{:15}'.format(str(row[1])) + '{:15}'.format( str(row[2]) + "$") \
            + '{:15}'.format(str(row[3]) + "$") + '{:15}'.format(str(row[4]))  + '\n'

    return stocks_string[:-1]

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
