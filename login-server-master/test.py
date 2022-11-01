import hashlib
import secrets

def hashPassword(password):
    #Add salt
    salt = secrets.token_hex(16)
    dataBase_password = password + salt
    # Hashing the password
    hashed = hashlib.sha512(dataBase_password.encode())
    print(salt)
    print(hashed.hexdigest())


hashPassword("bananas")