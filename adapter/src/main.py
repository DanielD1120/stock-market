import pymysql
import time
from influxdb import InfluxDBClient

db = None
influxdb = None
last_stock_change_id = 0

def connect_to_database():
    global db

    # Open database connection
    while True:
        try:
            db = pymysql.connect(host = "mysql-dev", user = "root", password = "password", db = "stocks")
            break
        except:
            continue

def select_last_stock_changes():
    global db

    connect_to_database()
    cursor = db.cursor()

    try:
        cursor.execute("select * from stock_prices_info")
    except pymysql.err.MySQLError as e:
        return "Error selecting last commands!\n" + str(e)

    rows = cursor.fetchall()
    cursor.close()
    db.close()

    return (rows, rows[len(rows) - 1][0])


def influxdb_connection():
	db_client = InfluxDBClient(host='influxdb', port=8086)
	db_client.create_database('stock_market')
	db_client.switch_database('stock_market')
	return db_client

def add_orders_to_influxdb(stock_market_changes):
    global influxdb

    current_points = []
    for change in stock_market_changes:
        current_point = {}
        current_point["measurement"] = change[1]
        tags = {}
        tags["price"] = "buy"
        current_point["tags"] = tags
        current_point["time"] = change[4]
        current_point["fields"] = {"value":change[2]}
        current_points.append(current_point)

    influxdb.write_points(current_points)

def main():
    global last_stock_change_id
    global influxdb

    time.sleep(10)
    influxdb = influxdb_connection()
    while True:
        changes, order_id = select_last_stock_changes()
        if order_id > last_stock_change_id:
            print("Adding new stock changes", flush=True)
            add_orders_to_influxdb(changes)
            last_stock_change_id = order_id
        time.sleep(5)

if __name__ == "__main__":
    main()

