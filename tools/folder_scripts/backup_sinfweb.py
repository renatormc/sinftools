import os
import requests

backup_storage_available = os.path.isdir("\\\\10.129.3.14\\sites")

if backup_storage_available:
    print("Backup storage already connected.")
else:
    print("Connecting to backup storage.")

    mount_command = "net use /user:sinf \\\\10.129.3.14\\sites iclrsinf"
    os.system(mount_command)
    backup_storage_available = os.path.isdir("\\\\10.129.3.14\\sites")

    if backup_storage_available:
        print("Connection success.")
    else:
        raise Exception("Failed to find storage directory.")

url = f"http://10.129.3.14/api/manutencao/backup"
print(url)
r = requests.get(url)
print(r.text)