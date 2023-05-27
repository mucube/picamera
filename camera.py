# This is the camera control code built with Pygame
import numpy as np
import cv2 as cv
import base64

import config
dummy_camera_data = config.get("dummy_camera_data")
device_names = dummy_camera_data.keys()

capture_dict = dict() #maps device names to their VideoCapture object

for device in device_names:
    capture_obj = cv.VideoCapture(dummy_camera_data[device][0])
    capture_dict[device] = capture_obj

def get_image_b64(device_name):
    ret, frame = capture_dict[device_name].read()
    _, im_arr = cv.imencode('.jpg', frame)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64

