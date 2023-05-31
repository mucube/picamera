# PiCamera

A simple and (probably) buggy software for remotely viewing security cameras. I created it to run on the Raspberry Pi, but you should be able to run it on any Linux distribution that uses Video4Linux.

## Features

* Should work on all Linux distributions
* It's a website, so you can view it remotely
* Authentication (for a single admin user)
* Settings

## Drawbacks

* Camera has to be directly attached to the machine, so no IP cameras (I don't even have one)
* No support for the Raspberry Pi camera module (I don't have one)
* (Probably) has lots of unforeseen bugs, but it does run fine on my machine
* Very hacky code that will probably break in the future (make sure you bleach your eyes after reading `camera_setup.py`)
* No support for multiple users

## Installing

First clone the GitHub repository:

```
git clone https://github.com/mucube/picamera.git
```

Then, run the setup script, which goes through the initial setup:

```
python3 setup.py
```

And follow the instructions from there.

## Running

Run `camera_setup.py`, and let it run in the background:

```
python3 camera_setup.py
```

If it throws an error, try again. For some reason (at least on my machine), it doesn't work first try most of the time, but it usually works the second time.


Then run `server.py`, which will also run in the background:

```
python3 server.py
```

## How It Works

In the backend, I'm using OpenCV to get the images for the browser camera feed, and ffmpeg for recording. Flask is used as the web server.

## License

PiCamera is licensed under the Apache License Version 2.0.
