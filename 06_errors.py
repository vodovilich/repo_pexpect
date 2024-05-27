import yaml
import pexpect
from pexpect.exceptions import ExceptionPexpect

SECRET_FILE_NAME = '06_secret.yml'

with open(SECRET_FILE_NAME, 'r') as f:
    creds = yaml.safe_load(f)

AIREOS_USERNAME = creds['AIREOS_USERNAME']
AIREOS_PASS = creds['AIREOS_PASS']
IOSXE_USERNAME = creds['IOSXE_USERNAME']
IOSXE_PASS = creds ['IOSXE_PASS']

def aireos_sh_cmd(ip, user, password, command):
    print(f"\n\nCONNECTING TO {ip}\n")
    with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
        index = ssh.expect(["User", "assword"])
        if index == 0:
            ssh.sendline(user)
        ssh.sendline(password)
        ssh.expect("\(Cisco Controller\)")
        ssh.sendline(command)
        output = ""
        while True:
            index = ssh.expect(["\(Cisco Controller\)", "--More--", "Press any key", pexpect.TIMEOUT], timeout=5)
            page = ssh.before
            output += page
            if index == 0:
                break
            elif index in [1, 2]:
                ssh.send(" ")
            else:
                print("Timeout")
                break
        return output.replace("\r", "")
  
    
def iosxe_sh_cmd(ip, user, password, command):
    print(f"\n\nCONNECTING TO {ip}\n")
    with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
        ssh.expect("#")
        ssh.sendline(command)
        ssh.expect("#")
        output=ssh.before
        return output.replace("\r", "")
        
def main():
    with open('06_devlist.yml', 'r') as f:
        devs = yaml.safe_load(f)
    for wlc in devs['aireos']:
        try:
            out = aireos_sh_cmd(wlc, AIREOS_USERNAME, AIREOS_PASS, "show int sum")
            for str in out.split("\n"):
                print(str)
        except (pexpect.exceptions.EOF, pexpect.exceptions.TIMEOUT) :
            print(f"Connection to {wlc} FAILED\n")
            continue

    for gw in devs['iosxe']:
        try:
            out = iosxe_sh_cmd(gw, IOSXE_USERNAME, IOSXE_PASS, "sh run | i hostname")
            for str in out.split("\n"):
                print(str)
        except (pexpect.exceptions.EOF, pexpect.exceptions.TIMEOUT):
            print(f"Connection to {wlc} FAILED\n")
            continue
          
if __name__ == "__main__":
    main()
    
"""
(venv-pexpect) gandalf@debian11:~/repo_pexpect$ python3 01_wlc.py 


CONNECTING TO 192.168.100.201

Connection to 192.168.100.201 FAILED



CONNECTING TO 192.168.100.9

Connection to 192.168.100.201 FAILED



CONNECTING TO 192.168.100.8

sh run | i hostname
hostname iol-157-01
iol-157-01
"""
