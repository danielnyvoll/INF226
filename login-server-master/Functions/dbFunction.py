import sys
import apsw
from apsw import Error

def run():
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
            id integer PRIMARY KEY, 
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            receiver TEXT NOT NULL,
            time TEXT NOT NULL);''')
        c.execute('''CREATE TABLE IF NOT EXISTS announcements (
            id integer PRIMARY KEY, 
            author TEXT NOT NULL,
            text TEXT NOT NULL);''')
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            userName TEXT NOT NULL PRIMARY KEY,
            password TEXT NOT NULL,
            salt TEXT NOT NULL);''')
        
        c.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', ('bob','d361a1eaf733a3ef1eacd4c1d4db259d8ac0f0dc7e4556615208bbf688b1d9aa4245a18a11c745e7883fbe956560e268d439476b95229a629e46ffb21f04072a','040b7e536674a317ae7c98a31958a5f7'))
        return conn
    except Error as e:
        print(e)
        sys.exit(1)
