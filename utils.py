import os
import subprocess

def cmd_output(cmd):
    '''Get output of command run in bash'''
    full_cmd = f'/bin/bash -c "{cmd}"'
    return subprocess.check_output(full_cmd, shell=True).decode('utf-8').strip()

def set_env(variable_name, value):
    '''Set Linux environment variable'''
    with open(os.path.expanduser("~/.bashrc"), "a") as f:
        f.write(f"\nexport {variable_name}={value}")

def get_env(variable_name):
    '''Get Linux environment variable'''
    return cmd_output(f"source ~/.bashrc && echo ${variable_name}")