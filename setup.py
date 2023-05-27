# Script to set config file
from werkzeug.security import generate_password_hash
import os

from utils import set_env
import camera_setup

# install some needed packages
print("installing packages...")
os.system("sudo apt-get install v4l-utils") #package is needed to view camera list
os.system("sudo apt-get install ffmpeg")
os.system("sudo apt-get install v4l2loopback-dkms") #for duplicating webcams so multiple apps can use it at the same time

os.system("python3 -m pip install --upgrade flask")
os.system("python3 -m pip install flask-login opencv-python")

config_path = input("Input the full path of the config.json file (this is very important): ")
set_env("PICAMERA_CONFIG_PATH", config_path)

import config

# set flask app's secret key
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

recording_path = input("Input the directory where the video recording will be stored (Make sure the directory exists, or else the recordings won't be stored!): ")
config.set("recording_path", recording_path)

camera_setup.setup()
print("Sucessfully set up cameras")

# add record_video.py to cron
os.system("chmod +x ./record_video.py")
os.system('(crontab -l 2>/dev/null; echo "0 * * * * $PWD/record_video.py") | crontab -') #https://stackoverflow.com/a/9625233
print("Record video job succesfully added to cron")

# add camera_setup.py to cron
os.system("chmod +x ./camera_setup.py")
os.system('(crontab -l 2>/dev/null; echo "@reboot $PWD/camera_setup.py") | crontab -') #https://stackoverflow.com/a/9625233
print("Camera setup job successfully added to cron")