# This is the camera control code built with Pygame
import pygame
import pygame.camera
from pygame.locals import *
import io
import base64

pygame.init()
pygame.camera.init()

class Capture:
    def __init__(self):
        self.running = False
        self.size = (640,480)

        # use the first camera in the camera list
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("No cameras detected")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)

        self.snapshot = pygame.surface.Surface(self.size, 0)
    
    def start(self):
        self.running = True
        self.cam.start()

    def get_image_b64(self):
        '''Get image data as JPEG base64 bytes'''
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        buffer = io.BytesIO()
        pygame.image.save(self.snapshot, buffer, "jpeg")
        b64_data = base64.b64encode(buffer.getvalue())
        return b64_data
    
    def stop(self):
        self.cam.stop()
        self.running = False
