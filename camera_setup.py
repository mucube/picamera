#!/bin/python3
# Set up the cameras and dummy cameras
# should be added to cron by the setup script
import os

import config
import subprocess

def setup():
    command_output = subprocess.run(["v4l2-ctl", "--list-devices"])
    number_of_cameras = len([i for i in command_output.splitlines()[:-1] if i != '' and i[0] != '\t'])

    # make two v4l2loopback dummy cameras for each camera so that one can be used by the browser video stream and one can be used for recording
    os.system("sudo modprobe v4l2loopback devices="+str(2*number_of_cameras))

    # extremely hacky code to detect connected cameras
    command_output = subprocess.run(["v4l2-ctl", "--list-devices"])
    lines = [i for i in command_output.splitlines()[:-1] if i != '']
    x = []
    for line in lines:
        if line[0] != '\t':
            x.append(line)
    command_output = command_output.replace('\t', '')
    for line in x:
        command_output = command_output.replace(line, '\t')
    splitted = [i for i in command_output.split('\t') if i != '']
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
    
    # copy the camera feed into the dummy cameras with ffmpeg
    for camera_device in dummy_camera_data.keys():
        dummy_cameras = dummy_camera_data[camera_device]
        os.system(f"ffmpeg -f video4linux2 -i {camera_device} -codec copy -f v4l2 {dummy_cameras[0]} -codec copy -f v4l2 {dummy_cameras[1]}")

    config.set("camera_data", camera_dict)
    config.set("dummy_camera_data", dummy_camera_data)

if __name__ == "__main__":
    setup()