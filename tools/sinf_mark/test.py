from sinf.servers.markers import get_scannable_drives
import psutil
import humanfriendly

res = get_scannable_drives()
for drive in res:
    drive = psutil.disk_usage(drive['drive'])
    print(f"Utilizado: {humanfriendly.format_size(drive.used, binary=True)}")
    