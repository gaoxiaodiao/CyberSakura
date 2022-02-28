from flask import Flask, render_template, url_for, request, redirect

import subprocess
import re
import string

app = Flask(__name__)

def is_valid_ip(ip):
    ipv = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\S{1,9})|(/s)\.(\d{1,3})$",ip)
    return bool(ipv)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        ip = request.form['content']
        if (is_valid_ip(ip)==True):
            for i in range(0,2):
                return '<pre>'+subprocess.check_output("ping -c 4 "+ip,shell=True).decode()+'</pre>'
                break
        else:
            return"That's not a valid IP"
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000) #8.8.8.8 - internet
# go to the main app and run ls and cat after the ip ping