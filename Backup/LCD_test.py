from lcddriver import *
from time import *
from GPS_init import *

def lcddisplay():
        lcd.lcd_clear();
        print("Displaying in LCD")
        lcd.lcd_display_string(string1, 1)
        lcd.lcd_display_string(string2, 2)
        while(1):
            pass
        
        
location = Gps()
lcd = lcddriver.lcd()
string1 = "%s"%str(getlocation.glat) + " " +"%s"%str(getlocation.glon)
string2 = "speed : %s"%str(getlocation.gspd)
print(string1)
print(string2)
lcd.lcd_clear();
lcddisplay()
