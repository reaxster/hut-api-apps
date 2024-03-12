import subprocess
import platform
from os import popen,system
import subprocess

def getUUID():
    os = platform.system()
    if os.lower() == "windows":
        cmd = str(popen('wmic path win32_computersystemproduct get uuid').read()).replace(" ", "").split("UUID")[1].strip()
        return cmd

    elif os.lower() == "linux":
        return str(popen('dmidecode -t system | grep UUID').read()).split("UUID:")[1].strip()
    else:
        raise Exception("SystemTypeNotFound")

def getOSType():
    return  platform.system()



#print(f"S/N : {str(subprocess.check_output('wmic bios get serialnumber').hex())}")
#print(f"UUID: ")