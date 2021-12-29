import datetime

alarmHour=int(input("What hour you'll take a lunch break? "))
alarmMinute=int(input("What minute you'll take a lunch break? "))
amPm=str(input("Am or PM? "))

if(amPm== "pm"):
    alarmHour = alarmHour + 12

while( 1 == 1):
    if (alarmHour == datetime.datetime.now().hour and alarmMinute == datetime.datetime.now().minute):
        print("Go take your lunch buddy!! ")
        break

print("Bon appetit!")
