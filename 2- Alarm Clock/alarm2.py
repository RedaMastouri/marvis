import sys
import time
import winsound

arguments = sys.argv

if len(arguments) != 2:
    print("Usage : [python] alarm2.py duration_in_minutes")
    print("Example : [python] alarm2.py 10")
    print("Alarm will be played after the duration is over")
    print("CTRL + C to stop the playing alarm")
    sys.exit(1)
try:
    minutes = int(arguments[1])
except:
    print("Invalid numeric value for duration in minutes")
    print("Should be >=0")
    sys.exit(1)

if minutes < 0:
    print("Value of duration in minutes should be >=0")
    sys.exit(1)

seconds = minutes * 60
try:
    if minutes > 0:
        print(f'Sleeping for {minutes} minutes')
        time.sleep(seconds)

    print('Take your lunch buddy!')


    # Codefor alarm
    for i in range(20):
        #winsound.Beep(1000,600)
        winsound.PlaySound('4.wav', winsound.SND_ASYNC)
        time.sleep(1)
except KeyboardInterrupt:
    print('Alarm turned off')
    sys.exit(1)


