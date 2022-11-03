import secrets
from Functions.hashFunction import getHashedPassword


def checkUsername(name, conn):
    users = conn.execute("SELECT userName FROM users").fetchall()
    for user in users:
        if name == user[0]:
            return True
    return False

def makeUser(username, password, conn):
    salt = secrets.token_hex(16)
    if(len(username)<3 or len(password)<8):
        return False
    if(username == "" or password == ""):
        return False
    if checkUsername(username, conn):
        return False
    else:
        password = getHashedPassword(password,salt)
        conn.execute("INSERT INTO users (username, password,salt) VALUES (?, ?, ?)", (username, password,salt))
        return True