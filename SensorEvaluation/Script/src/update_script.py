import json
import sys
import os
import logging
import requests
import psycopg2  # postgres interface

# Set needed settings
DB_HOST = os.environ[ 'DB_HOST' ]
DB_PORT = int(os.environ[ 'DB_PORT' ])
DB_NAME = os.environ[ 'DB_NAME' ]
DB_USER = os.environ[ 'DB_USER' ]
DB_PASSWD = os.environ[ 'DB_PASSWD' ]

LUFTDATEN_URL = "http://api.luftdaten.info/static/v1/data.json"

SQL_STMT_DELETE_SENSORDATAVALUES_AFTER_30_DAYS = "DELETE FROM sensordatavalues WHERE date < NOW()-'30 day'::INTERVAL"
SQL_STMT_DELETE_SENSORDATAVALUES_OLDEST_TWO_DAYS = "DELETE FROM sensordatavalues WHERE date < (SELECT MIN(date) from sensordatavalues)+'2 day'::INTERVAL"

SQL_STMT_GET_ALL_LOCATION_ID = "SELECT array_agg(id) FROM location"
SQL_STMT_GET_ALL_SENSOR_ID = "SELECT array_agg(id) FROM sensor"
SQL_STMT_GET_ALL_SENSORDATAVALUES_ID = "SELECT array_agg(id) FROM sensordatavalues"

SQL_STMT_INSERT_LOCATION = "INSERT INTO location(id, sensor_id, altitude, latitude, longitude, indoor, country) VALUES (%s, %s, %s, %s, %s, %s, %s)"
SQL_STMT_INSERT_SENSOR = "INSERT INTO  sensor(id, name, manufacturer) VALUES (%s, %s, %s)"
SQL_STMT_INSERT_SENSORDATAVALUES = "INSERT INTO sensordatavalues(id, sensor_id, value, value_type, date, time) VALUES (%s, %s, %s, %s, %s, %s)"


# input: string url
# output: JSON data (list) or empty string
def get_JSON_data(url):
    if url:
        try:
            resp = requests.get(url)
            data = json.loads(resp.text)
        except:
            data = ""
    else:
        data = ""
    return data

# input: object logging
# output: true if password is correct otlherwise false
def check_right_password_DB(log):
    conn = None
    try:
        conn = psycopg2.connect(
            database=DB_NAME, user=DB_USER, password=DB_PASSWD, host=DB_HOST, port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error(error)
        return False
    finally:
        if conn is not None:
            conn.close()
    return True

# input: string sql_stmt
# output: list of data from query or empty list
def get_all_data_DB(sql_stmt):
    conn = None
    try:
        conn = psycopg2.connect(
            database=DB_NAME, user=DB_USER, password=DB_PASSWD, host=DB_HOST, port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute(sql_stmt)
        result = cur.fetchall()[0][0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    if result is None:
        return []
    else:
        return result

# input: list insert_data, string sql_stmt
# output: nothing
def insert_data_DB(insert_data, sql_stmt):
    if insert_data:
        conn = None
        try:
            conn = psycopg2.connect(
                database=DB_NAME, user=DB_USER, password=DB_PASSWD, host=DB_HOST, port=DB_PORT
            )
            cur = conn.cursor()
            cur.executemany(sql_stmt, insert_data)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

# input: string sql_stmt
# output: nothing
def delete_data_DB(sql_stmt):
    conn = None
    try:
        conn = psycopg2.connect(
            database=DB_NAME, user=DB_USER, password=DB_PASSWD, host=DB_HOST, port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute(sql_stmt)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# input: list data
# output: adjust list of data or empty list
def prepare_sensor_data(data):
    if data and type(data) == type(list()):
        existing_sensor_ids = get_all_data_DB(SQL_STMT_GET_ALL_SENSOR_ID)
        data_list = []
        for d in data:
            if d["sensor"]["id"] not in existing_sensor_ids:
                # table sensor
                # id, name, manufacturer
                tup = (int(d["sensor"]["id"]), str(d["sensor"]["sensor_type"]["name"]), str(
                    d["sensor"]["sensor_type"]["manufacturer"]))
                data_list.append(tup)
                existing_sensor_ids.append(d["sensor"]["id"])
        return data_list
    else:
        return []

# input: list data
# output: adjust list of data or empty list
def prepare_location_data(data):
    if data and type(data) == type(list()):
        existing_sensor_ids = get_all_data_DB(SQL_STMT_GET_ALL_SENSOR_ID)
        existing_location_ids = get_all_data_DB(SQL_STMT_GET_ALL_LOCATION_ID)
        data_list = []
        for d in data:
            if (d["sensor"]["id"] in existing_sensor_ids) and (d["location"]["id"] not in existing_location_ids) and d["location"]["altitude"] and d["location"]["latitude"] and d["location"]["longitude"] and d["location"]["country"]:
                # table location
                # id, sensor_id, altitude, latitude, longitude, indoor, country
                tup = (int(d["location"]["id"]), int(d["sensor"]["id"]), float(d["location"]["altitude"]), float(d["location"]["latitude"]),
                       float(d["location"]["longitude"]), bool(d["location"]["indoor"]), str(d["location"]["country"]))
                data_list.append(tup)
                existing_location_ids.append(d["location"]["id"])

        return data_list
    else:
        return []

# input: list data
# output: adjust list of data or empty list
def prepare_sensordatavalues_data(data):
    if data and type(data) == type(list()):
        existing_sensor_ids = get_all_data_DB(SQL_STMT_GET_ALL_SENSOR_ID)
        data_list = []
        for d in data:
            for val in d["sensordatavalues"]:
                try:
                    if (d["sensor"]["id"] in existing_sensor_ids) and (str(val["value"]) not in "unavailable unknown null") and val["value"] and val["value_type"]:
                        splitted = d["timestamp"].split(" ")
                        # table sensordatavalues
                        # id, sensor_id, value, value_type, date, time
                        tup = (int(val["id"]), int(d["sensor"]["id"]), float(
                            val["value"]), str(val["value_type"]), splitted[0], splitted[1])
                        data_list.append(tup)
                except KeyError:
                    pass  # pressure_at_sealevel dont have a id

        return data_list
    else:
        return []

# input: object logging
# output: nothing
def main(log):
    log.info("Get data from luftdaten.info")
    data = get_JSON_data(LUFTDATEN_URL)
    log.info("Finish get data from luftdaten.info")

    log.info("Insert data about sensor")
    sensor_data = prepare_sensor_data(data)
    insert_data_DB(sensor_data, SQL_STMT_INSERT_SENSOR)
    log.info("Finish insert data about sensor")

    log.info("Insert data about location")
    location_data = prepare_location_data(data)
    insert_data_DB(location_data, SQL_STMT_INSERT_LOCATION)
    log.info("Finish insert data about location")

    log.info("Insert data about sensordatavalues")
    sensordatavalues_data = prepare_sensordatavalues_data(data)
    insert_data_DB(sensordatavalues_data, SQL_STMT_INSERT_SENSORDATAVALUES)
    log.info("Finish insert data about sensordatavalues")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.getLogger('pika').setLevel(logging.WARNING)
    log = logging.getLogger()

    if check_right_password_DB(log):
        log.info("Start the update process")
        main(log)
        log.info("Finish the update process")
    else:
        log.error("Connection to db did not work")
