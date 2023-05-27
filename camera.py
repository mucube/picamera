# This is the camera control code built with Pygame
import pygame
import pygame.camera
from pygame.locals import *
import io
import base64

import config

pygame.init()
pygame.camera.init()

class Capture:
    def __init__(self, device_name):
        self.size = (640,480)

        self.cam = pygame.camera.Camera(device_name, self.size)

        self.snapshot = pygame.surface.Surface(self.size, 0)

        self.cam.start()
        

    def get_image_b64(self):
        '''Get image data as BMP base64 bytes'''
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        buffer = io.BytesIO()
        pygame.image.save(self.snapshot, buffer, "bmp")
        b64_data = base64.b64encode(buffer.getvalue())
        return b64_data
dummy_camera_data = config.get("dummy_camera_data")
device_names = dummy_camera_data.keys()

capture_dict = dict() #maps device names to their capture object

for device in device_names:
    capture_obj = Capture(dummy_camera_data[device][0])
    capture_dict[device] = capture_obj

def get_image_b64(device_name):
    return capture_dict[device_name].get_image_b64()
