

#***********************************Easiest file operation***************************
#from shutil import copyfile

#copyfile("/home/pi/Project/Cofiguration files/record.txt", "/home/pi/Project/Cofiguration files/server.txt")



#************************************Difference of dates*****************************
import time
from datetime import datetime
from dateutil import parser

import linecache
line = linecache.getline("/home/pi/Project/record.txt", 13)
expiry_date = line[17:]
exp = parser.parse(expiry_date)
print("\n\nExpiry Date : %s\n")%exp
current_date = datetime.today().strftime('%d/%m/%Y')
current_date = parser.parse(current_date)
print("\n\nCurrent_date : %s\n")%current_date

delta = exp - current_date
print ("\n\nNumber of days left: %s\n")%delta.days
