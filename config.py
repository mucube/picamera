# Simple helper functions to get and set config entries
import json
d = dict()

with open("config.json", "r") as f:
    d = json.loads(f.read())

def get(entry_name):
    return d[entry_name]

def set(entry_name, value):
    d[entry_name] = value
    with open("config.json", "w") as f:
        f.write(json.dumps(d))