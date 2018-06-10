import time
import serial

CONTYPE = 'AT+SAPBR=3,1,"CONTYPE","GPRS"'
APN = 'AT+SAPBR=3,1,"APN","airtelgprs.com"'
SAPBR = 'AT+SAPBR=1,1'    
HTTPINIT = 'AT+HTTPINIT'
HTTPSTART = 'AT+HTTPPARA="CID",1'    
HTTPURL = 'AT+HTTPPARA="URL","http://api.thingspeak.com/update?api_key=Q5IJ589JWO5ZSHTP&field1=200'
HTTPACTION = 'AT+HTTPACTION=0'
CLSBR = 'AT+SAPBR=0,1'
HTTPTERM = 'AT+HTTPTERM'
class Gps:
    glat = 0;
    glon = 0;
    gspd = 0;
    gbal = 0;
    
    
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
        #c = self.phone.read(200)
        #if(c != ""):
        #print(c)
        
    def getlocation(self):
        Phone = self.phone
        try:
            #print("GPS function is Running")
            command = 'AT+CGNSINF'
            #command = raw_input('Enter the AT Command: ')
            #print('\n')
            Phone.write(command.encode() + b'\r')
            time.sleep(0.05)       
            c = Phone.read(200)
            if(c != ""):
                #print(c)
                lat = c.split(",")[3]
                #lat = float(lat)
                #print "latitude : %s" %lat
                lon = c.split(",")[4]
                #lon = float(lon)
                #print "longitude : %s" %lon
                spd = c.split(",")[6]
                #spd = float(spd)
                #print "Speed : %s\n\n" %spd
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
        #self.ATCmd = 'AT+SAPBR=3,1,"CONTYPE","GPRS"'
        phone.write(ATCmd.encode() + b"\r")
        time.sleep(0.05)
        c = phone.read(200)
        #if ENABLE_DEBUG == 1:
        if(c != ""):
            print(c)
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
        self.GPS_Send(CLSBR)                #Terminate any open connection
        self.GPS_Send(HTTPTERM)             #Terminate any open HTTP requests

        while(success != 0):
            if(Httpstate == CONTYPE):
                success = self.GPS_Send(CONTYPE)
                print("Going to APN")
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
        ATCOM = HTTPURL + '"' 
        ret = self.GPS_Send(HTTPSTART)
        if(ret):
            ret = self.GPS_Send(ATCOM)
            if(ret):
                ret = self.GPS_Send(HTTPACTION)
            



    








