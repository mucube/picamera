#!/bin/python3
# Script to record video of each camera for one hour
# should be added as a cron job by the setup script
import config
import os
import datetime

camera_data = config.get("camera_data")
dummy_camera_data = config.get("dummy_camera_data")
recording_path = "~/Videos/Recordings"

now = datetime.datetime.now()
one_hour_later = now + datetime.timedelta(hours=1)

for device in camera_data.values():
    os.system(f"ffmpeg -f v4l2 -i {device} -framerate 20 -t 01:00:00 -vcodec libx264 {recording_path}/recording-{device.replace('/dev/', '')}-{now.strftime('%Y-%m-%d')}-{now.strftime('%H_%M_%S')}-{one_hour_later.strftime('%H_%M_%S')}.mp4")
