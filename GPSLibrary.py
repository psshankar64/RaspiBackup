import time
import serial
ENABLE_DEBUG = 0

NULL = -1
CONTYPE = 'AT+SAPBR=3,1,"CONTYPE","GPRS"'
APN = 'AT+SAPBR=3,1,"APN","airtelgprs.com"'
SAPBR = 'AT+SAPBR=1,1'    
HTTPINIT = 'AT+HTTPINIT'
HTTPSTART = 'AT+HTTPPARA="CID",1'    
HTTPURL = 'AT+HTTPPARA="URL","http://api.thingspeak.com/update?api_key=Q5IJ589JWO5ZSHTP&field1='
HTTPURL2 = '&field2='
HTTPACTION = 'AT+HTTPACTION=0'
CLSBR = 'AT+SAPBR=0,1'
class Gps:
    glat = 0;
    glon = 0;
    gspd = 0;
    gbal = 0;
    resp = ""
    
    
    def OpenSerial(self):
        self.phone = serial.Serial("/dev/ttyAMA0",  baudrate=9600, timeout=5)
        if(self.phone.isOpen()):
            self.phone.close()
        self.phone.open()
        time.sleep(0.5)
        command = 'ATZ'
        self.phone.write(command.encode() + b'\r')
        command = 'AT+CGNSPWR=1'
        self.phone.write(command.encode() + b'\r')
        time.sleep(0.05)       
        c = self.phone.read(200)
        if(c != ""):
            if ENABLE_DEBUG == 1:
                print(c)
        
    def getlocation(self):
        Phone = self.phone
        try:
            command = 'AT+CGNSINF'
            Phone.write(command.encode() + b'\r')
            time.sleep(0.05)       
            c = Phone.read(200)
            if(c != ""):
                if ENABLE_DEBUG == 1:
                    print(c)
                lat = c.split(",")[3]
                lon = c.split(",")[4]
                spd = c.split(",")[6]
                #time.sleep(0.5)
                #locate = (lat,lon,spd)
                self.glat = lat
                self.glon = lon
                self.gspd = spd
                #return locate

        except KeyboardInterrupt:
            Phone.close()



    def GPS_Send(self,ATCmd):
        phone = self.phone
        self.phone.write(ATCmd.encode() + b"\r")
        time.sleep(0.05)
        c = phone.read(200)
        if(c != ""):
            if ENABLE_DEBUG == 1:
                print(c)
        if(c.find("HTTPACTION:") != NULL):
            self.resp = (c.split(":")[1])
        ret = self.check(c, ATCmd)
        return ret
    

    def check(self,c,ATCmd):
        if(c == ATCmd):
            return 1
        else:
            return ATCmd

    def HTTP_Init(self):
        phone = self.phone
        Httpstate = CONTYPE
        success = 1
        self.GPS_Send("AT+SAPBR=0,1")                  #Terminate any open connection
        self.GPS_Send("AT+HTTPTERM")                   #Terminate any open HTTP requests

        while(success != 0):
            if(Httpstate == CONTYPE):
                success = self.GPS_Send(CONTYPE)
                if(success):
                   Httpstate = APN
                else:
                    return success
                
            elif(Httpstate == APN):
                success = self.GPS_Send(APN)
                if(success):
                    Httpstate = SAPBR
                else:
                    return success

            elif(Httpstate == SAPBR):
                success = self.GPS_Send(SAPBR)
                if(success):
                    Httpstate = HTTPINIT
                else:
                    return success

            elif(Httpstate == HTTPINIT):
                success = self.GPS_Send(HTTPINIT)
                return success    


    def HTTP_CloseChannel(self):
        phone = self.phone
        success = self.GPS_Send(CLSBR)
        return success


    def DataHTTP(self):
        phone = self.phone 
        ATCOM = HTTPURL + str(float(self.gspd))+ HTTPURL2 + str(float(self.gspd)) + '"'
        ret = self.GPS_Send(HTTPSTART)
        if(ret):
            ret = self.GPS_Send(ATCOM)
            ret = self.GPS_Send(HTTPACTION)
            time.sleep(0.2)
            ret = self.GPS_Send("AT")
        

    def getbalance(self):
        balance = self.phone
        try:            
            command = 'AT+CUSD=1,"*123#"'
            #print('\n')
            balance.write(command.encode() + b'\r')
            time.sleep(0.05)       
            c = balance.read(200)
            if(c != ""):
                if ENABLE_DEBUG == 1:
                    print(c)
                bal = c.split(":")[2]                
                bal = bal.split("V")[0]
                bal = bal[3:]
                self.gbal = float(bal)

        except KeyboardInterrupt:
            balance.close()
               
    
















