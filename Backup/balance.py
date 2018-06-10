#!/usr/bin/env python

import time
import serial
#import re

balance = serial.Serial("/dev/ttyAMA0",  baudrate=9600, timeout=5)
balance.close()
balance.open()


class balance2:
        def getbalance(self):
                try:
                    
                        command = 'AT+CUSD=1,"*123#"'
                        #print('\n')
                        balance.write(command.encode() + b'\r')
                        time.sleep(0.05)       
                        c = balance.read(200)
                        if(c != ""):
                                #print(c)
                                bal = c.split(",")[2]
                                #print("Your account balance is :  %s\n")%bal
                                #bal2 = bal.split(".")[1]
                                bal2 = bal[:-11]
                                #print('balace : %s')%bal2
                                bal3 = bal2[-9:]
                                #print('balace : %s')%bal3
                                bal4 = bal2[-6:]
                                #print('Your balace : %s')%bal4
                                ybal = float(bal4)
                                if(ybal <= 200):
                                        print('Your balance %s is less than 200' +'\n'+ 'Kindly Recharge your Account\n')%ybal
                                else:
                                        print('You have sufficient balance')
                                 
                                
                               
                                     
                                time.sleep(0.5)

                except KeyboardInterrupt:
                    balance.close()
    
        #getbalance();
