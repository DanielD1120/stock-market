import requests
import time
import sys
import json
import re

server_host = "myserver:5000"
adminapp_host = "myadmin-app:5000"
priviledged_mode = False
current_user_name = None

def print_possible_commands():
    print("\nNormal operations:")
    print("1.  exit - exits client")
    print("2.  help - print this list")
    print("3.  create_acc user passwd")
    print("4.  login_admin user(char) passwd(char)")
    print("5.  login user(char) passwd(char)")
    print("6.  logout - log out of your account")
    print("7.  print - prints all current stocks")
    print("8.  get_my_stocks - prints all of your stocks")
    print("9.  add_money value - add money to your balance")
    print("10. sell_stock stock_name qty")
    print("11. buy_stock stock_name qty")
    print("12. add stock_name buy_price sell_price qty")
    print("13. update stock_name buy_price sell_price\n")

def print_stocks():
    url = "http://" + server_host + "/get_stocks"
    r = requests.get(url)
    try:
        print(r.json())
    except:
        print(r.text)

def login(cmd):
    global priviledged_mode
    global current_user_name
    info = cmd.split(' ')
    user = info[1]
    passwd = info[2]
    PARAMS = {"username"   : user, "password" : passwd}
    url = "http://" + server_host + "/login"
    r = requests.get(url, params= PARAMS)
    regex = re.compile("Login succesfull*")
    if regex.match(r.text):
        current_user_name = user
    print(r.text)

def create_acc(cmd):
    global priviledged_mode
    global current_user_name
    info = cmd.split(' ')
    user = info[1]
    passwd = info[2]
    PARAMS = {"username"   : user, "password" : passwd}
    url = "http://" + server_host + "/create_acc"
    r = requests.get(url, params= PARAMS)
    print(r.text)

def info(cmd):
    global current_user_name
    user = current_user_name
    PARAMS = {"username"   : user}
    url = "http://" + server_host + "/info"
    r = requests.get(url, params= PARAMS)
    print(r.text)

def add_money(cmd):
    global current_user_name
    info = cmd.split(' ')
    user = current_user_name
    money = info[1]
    PARAMS = {"username"   : user, "money" : money}
    url = "http://" + server_host + "/add_money"
    r = requests.get(url, params= PARAMS)
    print(r.text)

def get_my_stocks(cmd):
    global current_user_name
    user = current_user_name
    PARAMS = {"username"   : user}
    url = "http://" + server_host + "/get_my_stocks"
    r = requests.get(url, params= PARAMS)
    print(r.text)

def sell_stock(cmd):
    global current_user_name
    info = cmd.split(' ')
    user = current_user_name
    stock_name = info[1]
    qty = info[2]
    PARAMS = {"username"   : user, "stock_name" : stock_name, "quantity" : qty}
    url = "http://" + server_host + "/sell_stock"
    r = requests.get(url, params= PARAMS)
    print(r.text)

def buy_stock(cmd):
    global current_user_name
    info = cmd.split(' ')
    user = current_user_name
    stock_name = info[1]
    qty = info[2]
    PARAMS = {"username"   : user, "stock_name" : stock_name, "quantity" : qty}
    url = "http://" + server_host + "/buy_stock"
    r = requests.get(url, params= PARAMS)
    print(r.text)

def login_admin(cmd):
    global priviledged_mode
    info = cmd.split(' ')
    user = info[1]
    passwd = info[2]
    PARAMS = {"username"   : user, "password" : passwd}
    url = "http://" + adminapp_host + "/login"
    r = requests.get(url, params= PARAMS)
    if r.text == "Login succesfull!":
        priviledged_mode = True
    print(r.text)

# privileged operation
def add_stock(cmd):
    stocks_column = cmd.split(' ')

    try:
        _ = float(stocks_column[2])
        _ = float(stocks_column[3])
        _ = int(stocks_column[4])
    except ValueError:
        print("Values error")
        return

    PARAMS = {"stock_name"  : stocks_column[1],
              "buy_price"   : stocks_column[2],
              "sell_price"  : stocks_column[3],
              "qty"         : stocks_column[4]}

    url = "http://" + adminapp_host + "/add_stock"
    r = requests.put(url, params = PARAMS)
    print(r.text)

def update_stock(cmd):
    stocks_column = cmd.split(' ')

    try:
        _ = float(stocks_column[2])
        _ = float(stocks_column[3])
    except ValueError:
        print("Values error")
        return

    PARAMS = {"stock_name"  : stocks_column[1],
              "buy_price"   : stocks_column[2],
              "sell_price"  : stocks_column[3]}

    url = "http://" + adminapp_host + "/update_stock"
    r = requests.put(url, params = PARAMS)
    print(r.text)


def get_commands():
    global priviledged_mode
    global current_user_name

    print_possible_commands()

    while True:
        if priviledged_mode:
            line = input("admin$- ")
        else:
            if current_user_name:
                line_str = current_user_name + "$- "
                line = input(line_str)
            else:
                line = input("$- ")

        if line == "help":
            print_possible_commands()
        elif line == "exit":
            break
        elif line == "print":
            print_stocks()
        elif line == "logout":
            if priviledged_mode or current_user_name:
                priviledged_mode = False
                current_user_name = None
                print("Logout succesfull!")
            else:
                print("You are not logged in!")
        elif line.split(" ")[0] == "login_admin":
            if priviledged_mode or current_user_name:
                print("Logout before logging in!")
                continue
            if len(line.split(" ")) != 3:
                print("Not enough parameters or too many")
                print("login user passwd")
                continue
            login_admin(line)
        elif line.split(" ")[0] == "login":
            if priviledged_mode or current_user_name:
                print("Logout before logging in!")
                continue
            if len(line.split(" ")) != 3:
                print("Not enough parameters or too many")
                print("login user passwd")
                continue
            login(line)
        elif line.split(" ")[0] == "create_acc":
            if priviledged_mode or current_user_name:
                print("Logout before creating account!")
                continue
            if len(line.split(" ")) != 3:
                print("Not enough parameters or too many")
                print("create_acc user passwd")
                continue
            create_acc(line)
        elif line.split(" ")[0] == "info":
            if current_user_name:
                info(line)
            else:
                print("You are not logged in!")
        elif line.split(" ")[0] == "sell_stock":
            if current_user_name:
                if len(line.split(" ")) != 3:
                    print("Not enough parameters or too many")
                    print("sell_stock stock_name qty")
                    continue
                sell_stock(line)
            else:
                print("You are not logged in!")
        elif line.split(" ")[0] == "buy_stock":
            if current_user_name:
                if len(line.split(" ")) != 3:
                    print("Not enough parameters or too many")
                    print("buy_stock stock_name qty")
                    continue
                buy_stock(line)
            else:
                print("You are not logged in!")
        elif line.split(" ")[0] == "get_my_stocks":
            if current_user_name:
                get_my_stocks(line)
            else:
                print("You are not logged in!")
        elif line.split(" ")[0] == "add_money":
            if current_user_name:
                add_money(line)
            else:
                print("You are not logged in!")
        elif line.split(" ")[0] == "add":
            if priviledged_mode:
                if len(line.split(" ")) != 5:
                    print("Not enough parameters or too many")
                    print("add stock_name buy_price sell_price qty")
                    continue
                add_stock(line)
            else:
                print("You don't have permissions!")
        elif line.split(" ")[0] == "update":
            if priviledged_mode:
                if len(line.split(" ")) != 4:
                    print("Not enough parameters or too many")
                    print("update stock_name buy_price sell_price")
                    continue
                update_stock(line)
            else:
                print("You don't have permissions!")

if __name__ == "__main__":
    get_commands()
