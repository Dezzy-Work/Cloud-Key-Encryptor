import pymysql

from config.config import *

from tkinter import Tk
from tkinter import messagebox

con = pymysql.connect(
    host = host,
    port = 3306,
    user = user,
    password = password,
    database = db_name,
    cursorclass = pymysql.cursors.DictCursor
)

cur = con.cursor()

session_name = 0

def login(name, passw):
    try:
        name_for_sql = "SELECT * FROM `users` WHERE name = %s;"
        cur.execute(name_for_sql, (name,))
        value = cur.fetchall()

        value=value[1]

        if value == passw:
            global session_name
            session_name = name

            return 0

        else:
            Tk().withdraw()
            messagebox.showwarning("Alert", "Wrong login or password!")

            return 1


    except Exception:
        Tk().withdraw()
        messagebox.showwarning("Alert", "Wrong login or password!")

def register(name, passw):
    register_for_sql = "SELECT * FROM `users` WHERE name = %s;"

    cur.execute(register_for_sql, (name,))
    value = cur.fetchall()

    if value != ():
        Tk().withdraw()
        messagebox.showwarning("Alert", "This nickname is already in used!")

        return 1

    elif value == ():
        register_send_for_sql = "INSERT INTO `users` (name, password) VALUES (%s, %s);"

        line_length_password = str(len(passw))
        line_length_name = str(len(name))

        if int(line_length_name) >= 3:
            if int(line_length_password) >= 6:
                cur.execute(register_send_for_sql, (name, passw, ))
                con.commit()
                messagebox.showwarning("Alert", "You have successfully registered!")

                global session_name
                session_name = name

                return 0
            else:
                Tk().withdraw()
                messagebox.showwarning("Alert", "Minimum number of characters \n in password 6 characters")
        else: 
            Tk().withdraw()
            messagebox.showwarning("Alert", "Minimum number of characters \n in login 3 characters")

def write_key_of_db(key):
    try:
        send_key_of_db = "UPDATE `users` SET key_encoder = %s WHERE name = %s;"
        cur.execute(send_key_of_db, (key, session_name))
        con.commit()

        return 1
    except Exception:
        pass

def give_key_db():
    give_key_of_db = "SELECT key_encoder FROM users WHERE name = %s;"

    cur.execute(give_key_of_db, (session_name,))
    rows = cur.fetchall()

    for row in rows:

        return row[1]

def give_key_db_status():
    give_key_of_db_stat = "SELECT key_encoder FROM users WHERE name = %s;"

    cur.execute(give_key_of_db_stat)
    rows = cur.fetchall()

    if rows[1]:
        return 1
