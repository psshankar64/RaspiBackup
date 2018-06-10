#! /usr/bin/env python

# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LSM9DS0
# This code is designed to work with the LSM9DS0_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=LSM9DS0_I2CS#tabs-0-product_tabset-2

from math import sqrt, atan2, asin, degrees, radians
from GPSLibrary import Gps
from threading import *
from threading import Timer
from time import sleep
from datetime import datetime,timedelta
from dateutil import parser
from shutil import copyfile

import math
import smbus
import time 
import serial
import RPi.GPIO as GPIO
import cv2
import lcddriver
import sys
import linecache

ENABLE_DEBUG = 0
ENABLE_DEBUG2 = 0

#global ENABLE_DEBUG = 1



#**************************************************@SENDING MESSAGE****************************************************
def sendmessage():
        semaphore.acquire()
        print("Sending Message")
        recipient = "8884607032"
        message = "latitude is " + str(location.glat) +'\n' + "longitute is " + str(location.glon) + '\n' + "Speed is " +  str(location.gspd)
        terminate = "\x1A"
        phone = serial.Serial("/dev/ttyAMA0",  baudrate=9600, timeout=1)
        try:
                phone.write(b'AT+CMGS="8884607032"\r')
                time.sleep(0.5)
                c = phone.read(200)
                #time.sleep(0.5)
                #print(c)
                phone.write(message.encode())
                if ENABLE_DEBUG == 1:
                    print(c)
                phone.write(terminate.encode() + b'\r')
                time.sleep(0.5)
                c = phone.read(200)
                time.sleep(0.5)
                if ENABLE_DEBUG == 1:
                     print(c)
                semaphore.release()            
        finally:
            phone.close()


#*********************************************MAIN code goes here******************************************************

def getrollandpitch():
        #print('Getting roll and pitch')
        alpha = 0.5
        fxa = 0
        fya = 0
        fza = 0
        M_PI = 3.1415926535897
        count = 1

        while(1):
                semaphore.acquire()
                # LSM9DS0 Gyro address, 0x6A(106)
                # Select control register1, 0x20(32)
                #		0x0F(15)	Data rate = 95Hz, Power ON
                #					X, Y, Z-Axis enabled
                bus.write_byte_data(0x6b, 0x20, 0x0F)
                # LSM9DS0 address, 0x6A(106)
                # Select control register4, 0x23(35)
                #		0x30(48)	DPS = 2000, Continuous update
                bus.write_byte_data(0x6b, 0x23, 0x30)

                time.sleep(0.0005)

                # LSM9DS0 Gyro address, 0x6b(106)
                # Read data back from 0x28(40), 2 bytes
                # X-Axis Gyro LSB, X-Axis Gyro MSB
                data0 = bus.read_byte_data(0x6b, 0x28)
                data1 = bus.read_byte_data(0x6b, 0x29)

                # Convert the data
                xGyro = data1 * 256 + data0
                if xGyro > 32767 :
                        xGyro -= 65536
                Xg = xGyro

                # LSM9DS0 Gyro address, 0x6b(106)
                # Read data back from 0x2A(42), 2 bytes
                # Y-Axis Gyro LSB, Y-Axis Gyro MSB
                data0 = bus.read_byte_data(0x6b, 0x2A)
                data1 = bus.read_byte_data(0x6b, 0x2B)

                # Convert the data
                yGyro = data1 * 256 + data0
                if yGyro > 32767 :
                        yGyro -= 65536
                Yg = yGyro

                # LSM9DS0 Gyro address, 0x6A(106)
                # Read data back from 0x2C(44), 2 bytes
                # Z-Axis Gyro LSB, Z-Axis Gyro MSB
                data0 = bus.read_byte_data(0x6b, 0x2C)
                data1 = bus.read_byte_data(0x6b, 0x2D)

                # Convert the data
                zGyro = data1 * 256 + data0
                if zGyro > 32767 :
                        zGyro -= 65536
                Zg = zGyro

                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Select control register1, 0x20(32)
                #		0x67(103)	Acceleration data rate = 100Hz, Power ON
                #					X, Y, Z-Axis enabled
                bus.write_byte_data(0x1d, 0x20, 0x67)
                # LSM9DS0 Accl and Mag address, 0x1d(30)
                # Select control register2, 0x21(33)
                #		0x20(32)	Full scale = +/-16g
                bus.write_byte_data(0x1d, 0x21, 0x20)
                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Select control register5, 0x24(36)
                #		0x70(112)	Magnetic high resolution, Output data rate = 50Hz
                bus.write_byte_data(0x1d, 0x24, 0x70)
                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Select control register6, 0x25(37)
                #		0x60(96)	Magnetic full scale selection = +/-12 gauss
                bus.write_byte_data(0x1d, 0x25, 0x60)
                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Select control register7, 0x26(38)
                #		0x00(00)	Normal mode, Magnetic continuous conversion mode
                bus.write_byte_data(0x1d, 0x26, 0x00)

                time.sleep(0.0005)

                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Read data back from 0x28(40), 2 bytes
                # X-Axis Accl LSB, X-Axis Accl MSB
                data0 = bus.read_byte_data(0x1d, 0x28)
                data1 = bus.read_byte_data(0x1d, 0x29)

                # Convert the data
                xAccl = data1 * 256 + data0
                if xAccl > 32767 :
                        xAccl -= 65536
                Xa = xAccl
                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Read data back from 0x2A(42), 2 bytes
                # Y-Axis Accl LSB, Y-Axis Accl MSB
                data0 = bus.read_byte_data(0x1d, 0x2A)
                data1 = bus.read_byte_data(0x1d, 0x2B)

                # Convert the data
                yAccl = data1 * 256 + data0
                if yAccl > 32767 :
                        yAccl -= 65536
                Ya = yAccl

                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Read data back from 0x2C(44), 2 bytes
                # Z-Axis Accl LSB, Z-Axis Accl MSB
                data0 = bus.read_byte_data(0x1d, 0x2C)
                data1 = bus.read_byte_data(0x1d, 0x2D)

                # Convert the data
                zAccl = data1 * 256 + data0
                if zAccl > 32767 :
                        zAccl -= 65536
                Za = zAccl

                semaphore.release()
                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Read data back from 0x08(08), 2 bytes
                # X-Axis Mag LSB, X-Axis Mag MSB
                data0 = bus.read_byte_data(0x1d, 0x08)
                data1 = bus.read_byte_data(0x1d, 0x09)

                # Convert the data
                xMag = data1 * 256 + data0
                if xMag > 32767 :
                        xMag -= 65536

                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Read data back from 0x0A(10), 2 bytes
                # Y-Axis Mag LSB, Y-Axis Mag MSB
                data0 = bus.read_byte_data(0x1d, 0x0A)
                data1 = bus.read_byte_data(0x1d, 0x0B)

                # Convert the data
                yMag = data1 * 256 + data0
                if yMag > 32767 :
                        yMag -= 65536

                # LSM9DS0 Accl and Mag address, 0x1E(30)
                # Read data back from 0x0C(12), 2 bytes
                # Z-Axis Mag LSB, Z-Axis Mag MSB
                data0 = bus.read_byte_data(0x1d, 0x0C)
                data1 = bus.read_byte_data(0x1d, 0x0D)
                
                
                # Convert the data
                zMag = data1 * 256 + data0
                if zMag > 32767 :
                        zMag -= 65536


                fxa = Xa * alpha + (fxa * (1.0 - alpha))
                fya = Ya * alpha + (fya * (1.0 - alpha))
                fza = Za * alpha + (fza * (1.0 - alpha))

                roll  = (atan2(fxa,fza))*57.2958
                pitch = (atan2(fya,fza))*57.2958
                heading = (atan2(fxa,fya)*57.2958)+180

                roll = float("{0:.3f}".format(roll))
                pitch = float("{0:.3f}".format(pitch))
                heading = float("{0:.3f}".format(heading))

                if(roll>=85 or pitch>=85 or roll<=-85 or pitch<=-85): #or heading >=90):
                        
                        GPIO.output(buzz_PIN, True)
                        #sendmessage();
                        #from shutil import copyfile
                        #copyfile("/home/pi/Project/record.txt", "/home/pi/Project/server.txt")
                        for count in range(15):
                                print("Capturing Photos %d")%count
                                cam = cv2.VideoCapture(0)
                                ret, image = cam.read()
                                if ret:
                                        w = 1024
                                        h = 768
                                        cam.set(3,w)
                                        cam.set(4,h)
                                        im_name = "/home/pi/book/output/image" + str(count) +".jpg"
                                        #cv2.waitKey(0)
                                        cv2.imwrite(im_name,image)
                                        cam.release()
                                        time.sleep(0.3)
                        lcd.lcd_clear();
                        lcd.lcd_display_string("Photos Taken", 1)
                        
                else:
                        GPIO.output(buzz_PIN, False)
                if ENABLE_DEBUG2 == 1:
                        print '            ','Roll:',roll,'            ','Pitch:',pitch,'              ','Heading:',heading,'\n\n'
                        print("\n")
                
#********************************************************LCD Display Function**************************************
def GPSThread():
        count = 1
        while(1):
                location.getlocation()
                semaphore.acquire()
                lcd.lcd_clear();
                #string1 = "%s"%str(location.glat) + " " +"%s"%str(location.glon)
                string2 = "speed : %s"%str(location.gspd)
                time.sleep(0.2)
                semaphore.release()
                if(count <= 5):
                        if ENABLE_DEBUG == 1:
                                print("Counting %s")%count
                        count1 = ("count : %d")%count
                        lcd.lcd_clear();
                        lcd.lcd_display_string(str(count1), 1)
                        lcd.lcd_display_string(string2, 2)
                        #time.sleep(0.5)
                        count = count + 1
                        pass
                else:
                        lcd.lcd_clear();
                        lcd.lcd_display_string("Getting Server", 1)
                        lcd.lcd_display_string("Response", 2)
                        #lcd.lcd_clear();
                        location.DataHTTP()
                        if ENABLE_DEBUG == 1:
                                print("Log action Returned: %s")%location.resp
                        lcd.lcd_clear();
                        display = ("Status:%s")%str(location.resp)
                        lcd.lcd_display_string(display, 1)
                        time.sleep(1)
                        lcd.lcd_clear();
                        lcd.lcd_display_string("UPDATING GPS", 1)
                       
                        count = 1





#**************************************************@Buzz config********************************************************
buzz_PIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzz_PIN, GPIO.OUT)
#**************************************************@Getting I2C bus****************************************************
bus = smbus.SMBus(1)

#*****************************************************@LCD Init********************************************************
lcd = lcddriver.lcd()
lcd.lcd_clear();


#*****************************************************@Checking Insurence validity********************************************************
line = linecache.getline("/home/pi/Project/record.txt", 13)
expiry_date = line[17:]
exp = parser.parse(expiry_date)
#print("\n\nExpiry Date : %s\n")%exp
#alert_sent_on = datetime.strptime(alert_sent_on, "%d/%m/%Y")
current_date = datetime.today().strftime('%d/%m/%Y')
current_date = parser.parse(current_date)
#print("\n\nCurrent_date : %s\n")%current_date

delta = exp - current_date
#print ("\n\nNumber of days left: %s\n")%delta.days
if(float(delta.days)<=45):
        print("\n\n\tYour Bike Insurance is Expiring in %s days, Please Renew it......\n\n")%delta.days
else:
        print("Insurance Valid till %s")%exp



#***************************************@GPS Init and SIM balance display**********************************************
time.sleep(1)
location = Gps()
lcd.lcd_clear();
lcd.lcd_display_string("Setting up", 1)
lcd.lcd_display_string("your System", 2)
time.sleep(1)
location.OpenSerial()
location.HTTP_Init()
location.OpenSerial()
location.getbalance()
string1 = "Sim Balance"
#print(location.gbal)
if(location.gbal < 20.0 and location.gbal > 5.0):        
        string2 = "Low : %s"%str(location.gbal)
elif(location.gbal <= 5.0):
        
        string2 = "NIL : %s"%str(location.gbal)
else:
        string2 = "Good : %s"%str(location.gbal) 
        
lcd.lcd_display_string(string1, 1)
lcd.lcd_display_string(string2, 2)
time.sleep(3)
#getServer()
#********************************************************Start the main threads*****************************************
if ENABLE_DEBUG == 1:
        print("Starting the Threads\n")
t1 = Thread(target = getrollandpitch)
t2 = Thread(target = GPSThread)
semaphore = Semaphore()
t1.daemon = True
t2.daemon = True


if(t1):
        t1.start()
if(t2):
        t2.start()
while(1):
        try:                
                pass
        except KeyboardInterrupt:
                sys.exit()
        


        

