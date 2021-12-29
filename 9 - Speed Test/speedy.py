# checking internet access with speedtest-cli
import os
try:
    os.system('cmd /k "speedtest-cli --simple"')
 
except:
    print('Checkput your internet connection!')