import pexpect

def send_show_command(ip, user, password, command):
    with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
        ssh.expect("assword")
        
        ssh.sendline(password)
        ssh.expect("#")
        
        ssh.sendline('terminal length 0')
        ssh.expect("#")
        
        ssh.sendline(command)
        ssh.expect('#')
        output = ssh.before + ssh.after
        return output

if __name__ == "__main__":
    ip_list = ["192.168.100.24", "192.168.100.27"]
    for ip in ip_list:
        print(f"\n\nCONNECTING TO {ip}")
        print(send_show_command(ip, "gandalf", "grey", "sh ip int br"))
        
"""
Default output - one string presented in bytes (you can see 'b' symbols) with /r and /n symbols.
To eliminate this -  encoding="utf-8" is used
To see that shit : 
    from pprint import pprint
    return output.re[;ace("\r\n","\n")]
    pprint(send_show_command("192.168.100.27", "gandalf", "grey", "sh ip int br"))
"""