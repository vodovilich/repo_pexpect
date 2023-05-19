import pexpect, re, getpass
from pprint import pprint
"""
PREREQUESITES:
-list of hosts is already known in ip_list list
-RADIUS AUTHN on target hosts
"""

passw = getpass.getpass('Password: ')

def send_show_commands(ip, user, password):
    with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
        index = ssh.expect(["User", "assword"])
        if index == 0:
            ssh.sendline(user)       
        ssh.sendline(passw)
        ssh.expect(">")
        
        ssh.sendline("show interface summary")
        ssh.expect(">")
        output = ssh.before
        
        for str in output.split("\n"):
            if '2400' in str:
                ifname = str.split()[0]
        print("Interfaces are going to be modified:")
        print(ifname)      
        
        print("YOU WANT TO GO WITH COMMAND:")
        print(f"config interface delete {ifname}")
        
        ssh.sendline(f"config interface delete {ifname}")
        ssh.expect(">")
        buff = ssh.before
        print(buff)
        ssh.sendline("save config")
        ssh.expect("Are you sure")
        buff = ssh.before
        print(buff)
        
        ssh.sendline("y")
        ssh.expect(">")
        buff = ssh.before
        print(buff)
        
        ssh.expect(">")
        ssh.sendline("logout")
        buff = ssh.before
        print(buff)


 
if __name__ == "__main__":
    ip_list = ["rokhan-wlc01", "shire-wlc01", "helmsfall-wlc01", "mns-tirith-wlc01", "nms-morgul-wlc01", "isengard-wlc01"]
    for ip in ip_list:
        print(f"\n\n\nCONNECTING TO {ip}")
        send_show_commands(ip, "gandalf", passw)
