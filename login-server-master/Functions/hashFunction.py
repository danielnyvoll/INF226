# Helper function for hashing the password user input with salt 
import hashlib


def getHashedPassword(password, salt):
    password += salt
    return hashlib.sha512(password.encode()).hexdigest()