import os
import sys

if sys.argv[1] == 'ssp':
    os.system("netsh wlan disconnect")
    os.system("netsh interface set interface \"SSP\" ENABLED")
    # user_password = os.getenv("PROXYPWD")
    # if user_password:
    #     os.system(f"setx HTTP_PROXY http://{user_password}@webgateway.ssp.go.gov.br:8080")
    #     os.system(f"setx HTTPS_PROXY http://{user_password}@webgateway.ssp.go.gov.br:8080")
elif sys.argv[1] == 'adsl':
    os.system("netsh interface set interface \"SSP\" DISABLE")
    os.system("netsh wlan connect name=\"INF\"")
elif sys.argv[1] == 'fibra2G':
    os.system("netsh interface set interface \"SSP\" DISABLE")
    os.system("netsh wlan connect name=\"LIVE TIM_0002_2G\"")
elif sys.argv[1] == 'fibra5G':
    os.system("netsh interface set interface \"SSP\" DISABLE")
    os.system("netsh wlan connect name=\"LIVE TIM_0002_5G\"")
    # os.system("setx HTTP_PROXY \"\"")
    # os.system("setx HTTPS_PROXY \"\"")
  
    
    