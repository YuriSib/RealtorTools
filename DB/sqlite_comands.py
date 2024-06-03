import sqlite3
from sqlite3 import Error
import json

import sql_commands as sql_com


def open_db():
    conn = sqlite3.connect('realtors.db')
    cursor = conn.cursor()
    cursor.execute(sql_com.create_db)
    return conn, cursor


def add_user(name, tg_id):
    conn, cursor = open_db()
    cursor.execute("INSERT INTO users (name, tg_id) VALUES (?, ?)", (name, tg_id))
    conn.commit()
    conn.close()


def add_filter_1(tg_id, filter_1_value):
    conn, cursor = open_db()

    cursor.execute(f"SELECT filter_1 FROM users WHERE tg_id = {tg_id}")
    row = cursor.fetchall()
    if row[0][0]:
        value_list = json.loads(row[0][0])
        value_list.append(filter_1_value)
        filter_1_json = json.dumps(value_list)
    else:
        filter_1_json = json.dumps([filter_1_value])

    cursor.execute("UPDATE users SET filter_1 = ? WHERE tg_id = ?", (filter_1_json, tg_id))
    conn.commit()
    conn.close()


def get_filter_1(tg_id):
    conn, cursor = open_db()

    cursor.execute(f"SELECT filter_1 FROM users WHERE tg_id = {tg_id}")
    row = cursor.fetchall()
    conn.close()

    return json.loads(row[0][0])


if __name__ == "__main__":
    filter_1 = '355'
    tg_id = 121345124
    user_name = 'ASD'

    # add_user(user_name, tg_id)
    add_filter_1(tg_id, filter_1)
