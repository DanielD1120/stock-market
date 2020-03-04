import requests
import time
import sys
import json

server_host = "myserver:5000"
adminapp_host = "myadmin-app:5000"
priviledged_mode = False

def print_possible_commands():
    print("\nNormal operations:")
    print("exit - exits client")
    print("help - print this list")
    print("login user(char) passwd(char) - enter priviledged mode")
    print("logout - log out of priviledged mode")
    print("print - prints current stocks")
    print("add stock_name buy_price sell_price - add a stock to the stock market")
    print("update stock_name buy_price sell_proce - update a stock price")

def print_stocks():
    url = "http://" + adminapp_host + "/get_stocks"
    r = requests.get(url)
    try:
        print(r.json())
    except:
        print(r.text)

def login(cmd):
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
        _ = int(stocks_column[2])
        _ = int(stocks_column[3])
    except ValueError:
        print("Values error")
        return

    PARAMS = {"stock_name"  : stocks_column[1],
              "buy_price"   : stocks_column[2],
              "sell_price"  : stocks_column[3]}

    url = "http://" + adminapp_host + "/add_stock"
    r = requests.put(url, params = PARAMS)
    print(r.text)

def update_stock(cmd):
    stocks_column = cmd.split(' ')

    try:
        _ = int(stocks_column[2])
        _ = int(stocks_column[3])
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
    print_possible_commands()

    while True:
        if priviledged_mode:
            line = input("admin$- ")
        else:
            line = input("$- ")

        if line == "help":
            print_possible_commands()
        elif line == "exit":
            break
        elif line == "print":
            print_stocks()
        elif line == "logout":
            if priviledged_mode:
                priviledged_mode = False
                print("Logout succesfull!")
            else:
                print("You are not logged in!")
        elif line.split(" ")[0] == "login":
            if len(line.split(" ")) != 3:
                print("Not enough parameters or too many")
                print("login user passwd - enter priviledged mode")
                continue
            login(line)
        elif line.split(" ")[0] == "add":
            if priviledged_mode:
                if len(line.split(" ")) != 4:
                    print("Not enough parameters or too many")
                    print("add stock_name buy_price sell_price")
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
