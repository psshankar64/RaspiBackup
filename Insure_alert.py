from datetime import datetime


alert_sent_on = datetime.today().strftime('%d/%m/%Y')
if(alert_sent_on):
    updated = 1

#alert_sent_on = datetime.strptime(alert_sent_on, "%d/%m/%Y")
#print(alert_sent_on)

