import requests


files = {'file': open(r'C:\Users\renato\Pictures\Memmoria kabum.PNG', "rb")}
response = requests.post("http://localhost:8000/servers/upload-file", files=files)
print(response.text)