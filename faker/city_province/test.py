import datetime as dt
HOUR_CHOICES = [(None, '------')]
for hour in range(0,12):
    for minute in range(0,46,15):
        tup = (str(dt.time(hour=hour, minute=minute)), str(hour)+":"+str(minute)+" AM")
        HOUR_CHOICES.append(tup)



for hour in range(12,24):
    for minute in range(0,46,15):
        tup = (str(dt.time(hour=hour, minute=minute)), str(int(hour-12))+":"+str(minute)+" PM")
        HOUR_CHOICES.append(tup)
print(HOUR_CHOICES)