
from Insure_alert import alert_sent_on
from datetime import datetime, timedelta
#today = datetime.today().strptime('%d/%m/%Y')

alert_sent_on = datetime.strptime(alert_sent_on, "%d/%m/%Y")
next_display = alert_sent_on + timedelta(days=50)
#print(next_display)
#next_display = datetime.strptime(next_display, "%d/%m/%Y")
today = str(datetime.today().strftime('%d/%m/%Y'))
today = datetime.strptime(today, "%d/%m/%Y")

#alert_sent_on = today
#if(alert_sent_on):
#    updated = 1

    
if(alert_sent_on < next_display):
    if(updated = 1)
    if(alert_sent_on == today):
        #updated = 1
        pass
    else:
        next_display = alert_sent_on - timedelta(days=1)
        updated = 0
        pass

else:
    print("Sending alert")
    print("\n\n\tYour Bike Insurance is Expiring in %s days, Please Renew it......\n\n")%timedelta.days
    next_display = alert_sent_on + timedelta(days=15)
