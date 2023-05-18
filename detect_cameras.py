# extremely hacky script to detect connected cameras
import subprocess

def get_camera_data():
    cmd_output = subprocess.check_output(['v4l2-ctl', '--list-devices']).decode('utf-8')
    lines = cmd_output.splitlines()[:-1]
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
    return camera_dict