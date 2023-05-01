import pexpect
from pprint import pprint

def send_show_command(ip, user, password, command):
    print(f"\n\nCONNECTING TO {ip}")
    with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
        ssh.expect("User")
        
        ssh.sendline(user)        
        ssh.expect("assword")
                
        ssh.sendline(password)
        ssh.expect("\(Cisco Controller\)")
        
        ssh.sendline('terminal length 0')
        ssh.expect("\(Cisco Controller\)")
        
        ssh.sendline(command)
        output = ""
        while True:
            index = ssh.expect(["\(Cisco Controller\)", "--More--", pexpect.TIMEOUT], timeout=5)
            page = ssh.before
            output += page
            if index == 0:
                break
            elif index ==1:
                ssh.send(" ")
                #sendline adds \n, send does not
            else:
                print("Timeout")
                break
        return output.replace("\r", "")

if __name__ == "__main__":
    ip_list = ["cisco2500-wlc01", "cisco2500-wlc02"]
    for ip in ip_list:
        out = send_show_command(ip, "gandalf", "grey", "show ap join stats summary all")
        #pprint(out, width = 120)
        print(out)
        



    
    