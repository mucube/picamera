# Script to set config file
from werkzeug.security import generate_password_hash
import os

distro = input("""Input the number of the Linux distribution you are using:
1. Debian (includes Ubuntu and Raspberry Pi OS)
2. Arch Linux
""")

# install some needed packages
print("installing packages...")
if distro == "1":
    os.system("sudo apt-get install v4l-utils") #package is needed to view camera list
    os.system("sudo apt-get install ffmpeg")
    os.system("sudo apt-get install v4l2loopback-dkms") #for duplicating webcams so multiple apps can use it at the same time
elif distro == "2":
    os.system("sudo pacman -S v4l-utils")
    os.system("sudo pacman -S ffmpeg")
    os.system("sudo pacman -S v4l2loopback-dkms")
else:
    print("You entered an invalid input. Exiting.")
    quit()

os.system("python3 -m pip install --upgrade flask")
os.system("python3 -m pip install flask-login opencv-python")

try:
    os.mkdir(os.path.expanduser("~/.config/picamera"))
except FileExistsError: #if the directory already exists
    pass

with open(os.path.expanduser("~/.config/picamera/config.json"), "w") as f:
    f.write("{}")

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

recording_path = input("Input the directory where the video recording will be stored: ")
try:
    os.mkdir(os.path.expanduser(recording_path))
except FileExistsError: #if the directory already exists
    pass
config.set("recording_path", os.path.expanduser(recording_path))

# add record_video.py to cron
#os.system("chmod +x ./record_video.py")
#os.system('(crontab -l 2>/dev/null; echo "0 * * * * $PWD/record_video.py") | crontab -') #https://stackoverflow.com/a/9625233
#print("Record video job succesfully added to cron")

# add camera_setup.py to cron
#os.system("chmod +x ./camera_setup.py")
#os.system('(crontab -l 2>/dev/null; echo "@reboot $PWD/camera_setup.py") | crontab -') #https://stackoverflow.com/a/9625233
#print("Camera setup job successfully added to cron")