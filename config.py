# Simple helper functions to get and set config entries
import json
import os
d = dict()

config_path = os.path.expanduser("~/.config/picamera/config.json")

try:
    with open(config_path, "r") as f:
        d = json.loads(f.read())
except (FileNotFoundError, json.decoder.JSONDecodeError) as e: # if there is no config.json file or it is not in valid json
    with open(config_path, "w") as f:
        f.write("{}")

def get(entry_name):
    return d[entry_name]

def set(entry_name, value):
    d[entry_name] = value
    with open(config_path, "w") as f:
        f.write(json.dumps(d))
