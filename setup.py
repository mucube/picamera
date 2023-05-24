# Script to set config file
from werkzeug.security import generate_password_hash
import os
import subprocess

# install some needed packages
print("installing packages...")
os.system("sudo apt-get install v4l-utils") #package is needed to view camera list
os.system("sudo apt-get install ffmpeg")
os.system("sudo apt-get install v4l2loopback-dkms") #for duplicating webcams so multiple apps can use it at the same time

os.system("python3 -m pip install --upgrade pygame flask")
os.system("python3 -m pip install flask-login")

#config_path = input("Input the full path to the config.json file (if it doesn't exist it will be created): ")
#os.environ["PICAMERA_CONFIG_PATH"] = config_path

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

number_of_cameras = int(input("How many cameras are connected to the Raspberry Pi? (PiCamera will use the video output from all of them, so please input this correctly.)"))
# make two v4l2loopback dummy cameras for each camera so that one can be used by the browser video stream and one can be used for recording
os.system("sudo modprobe v4l2loopback devices="+str(2*number_of_cameras))

# extremely hacky code to detect connected cameras
cmd_output = subprocess.check_output(['v4l2-ctl', '--list-devices']).decode('utf-8')
lines = [i for i in cmd_output.splitlines()[:-1] if i != '']
x = []
for line in lines:
    if line[0] != '\t':
        x.append(line)
cmd_output = cmd_output.replace('\t', '')
for line in x:
    cmd_output = cmd_output.replace(line, '\t')
splitted = [i for i in cmd_output.split('\t') if i != '']
camera_dict = dict()
for i in range(len(x)):
    name = x[i][:-1]
    y = [i for i in splitted[i].splitlines() if i != ''][0]
    camera_dict[name] = y
# more hacky code to get the device driver names of each of the dummy cameras
dummy_cameras = [] # device driver names of the v4l2loopback dummy cameras
camera_names = list(camera_dict.keys())
for camera_name in camera_names:
    if "Dummy video device" in camera_name and "platform:v4l2loopback" in camera_name:
        dummy_cameras.append(camera_dict[camera_name])
        del camera_dict[camera_name]

# even more hacky code to map each camera to two dummy cameras
dummy_camera_data = dict() # maps each real cameras to its dummy cameras
dummy_cameras2 = dummy_cameras
for camera in camera_dict.values():
    dummy_camera_data[camera] = dummy_cameras2[:2]
    dummy_cameras2 = dummy_cameras2[2:]

config.set("camera_data", camera_dict)
config.set("dummy_camera_data", dummy_camera_data)
print("Sucessfully retrieved camera data")

# add record_video.py to cron
os.system("chmod +x ./record_video.py")
os.system('(crontab -l 2>/dev/null; echo "0 * * * * $PWD/record_video.py -with args") | crontab -') #https://stackoverflow.com/a/9625233
print("Record video job succesfully added to cron")
