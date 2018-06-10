from http_req import Gps


location = Gps()

location.OpenSerial()


ans1 = location.HTTP_Init()
print(ans1)
location.DataHTTP()
ans2 = location.HTTP_CloseChannel()
#print(ans2)
