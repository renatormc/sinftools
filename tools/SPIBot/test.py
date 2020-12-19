from com.dtmilano.android.viewclient import ViewClient

device, serialno = ViewClient.connectToDeviceOrExit()
ViewClient.sleep(2)
vc = ViewClient(device, serialno)
# vc.click(50, 1370)
# vc.writeImageToFile("c:\\temp\\teste.png")