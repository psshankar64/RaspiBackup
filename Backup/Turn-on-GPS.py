#!/usr/bin/env python

import time
import serial

phone = serial.Serial("/dev/ttyAMA0",  baudrate=9600, timeout=5)
if(phone.isOpen()):
    phone.close()
phone.open()

try:
    while(1):
        command =  'AT+CGNSINF' #raw_input('Enter the AT Command: ')
        phone.write(command.encode() + b'\r')
        time.sleep(0.05)       
        c = phone.read(200)
        if(c != ""):
            print(c)
            lat = c.split(",")[3]
            lon = c.split(",")[4]
            spd = c.split(",")[6]
        print(lat)
        time.sleep(0.5)

except KeyboardInterrupt:
    phone.close()
