# Script to set config file
from werkzeug.security import generate_password_hash
import config
import os

import detect_cameras

def set_password():
    password = input("Type admin password (please make it unique): ")
    retyped_password = input("Re-type admin password: ")
    if password == retyped_password:
        password_hash = generate_password_hash(password)
        config.set("password_hash", password_hash)
    else:
        print("The passwords did not match, please try again")
        set_password()


# install some needed packages
print("installing packages...")
os.system("sudo apt-get install v4l-utils") #package is needed to view camera list

os.system("python3 -m pip install --upgrade pygame flask")
os.system("python3 -m pip install flask-login")

# set flask app's secret key
config.set("secret_key", os.urandom(16).hex())

set_password()

def set_view_perm():
    perm_input = input("Should everyone be allowed to view the camera feed? y/n ")
    if perm_input == "y" or perm_input == "yes":
        config.set("view_perm", True)
    elif perm_input == "n" or perm_input == "no":
        config.set("view_perm", False)
    else:
        print("That was an invalid input. Enter again.")
        set_view_perm()

set_view_perm()

config.set("camera_data", detect_cameras.get_camera_data()) # store camera data