import subprocess

def get_drives_linux():
    mount = subprocess.getoutput('mount -v')
    lines = mount.split('\n')
    points = []
    for line in lines:
        if line.startswith("/dev/sd"):
            points.append(line.split()[2])
    return points
    
for item in get_drives_linux():
    print(item)
# print(mounts)