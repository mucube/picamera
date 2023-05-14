# Script to set config file
from werkzeug.security import generate_password_hash
import config
import os

def set_secret_key():
    config.set("secret_key", os.urandom(16).hex())

def set_password():
    password = input("Type admin password (please make it unique): ")
    retyped_password = input("Re-type admin password: ")
    if password == retyped_password:
        password_hash = generate_password_hash(password)
        config.set("password_hash", password_hash)
    else:
        print("The passwords did not match, please try again")
        set_password()

set_secret_key()
set_password()