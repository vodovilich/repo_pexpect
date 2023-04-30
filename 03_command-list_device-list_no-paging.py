import pexpect
from pprint import pprint

def send_show_commands(ip, user, password, commands):
    cmd_output_dict = {}
    with pexpect.spawn(f"ssh {user}@{ip}", timeout=20, encoding="utf-8") as ssh:
        ssh.expect("User")
        #LOGIN TO CISCO WITH EXEC-AUTH PASSWORD 
        #ssh.sendline(user)        
        ssh.expect("assword")
        
        ssh.sendline(password)
        ssh.expect("#")
        
        
        if type(commands) == str:
            commands = [commands]
        
        for cmd in commands:
            ssh.sendline(cmd)
            #ssh.expect("\(Cisco")
            ssh.expect("\S+#")            
            output = ssh.before
            output = output.replace("\r", '')
            cmd_output_dict[cmd] = output
        return cmd_output_dict
    
if __name__ == "__main__":
    ip_list = ["192.168.100.24", "192.168.100.27"]
    com_list =  ["show inventory", "show ip int br"]
    for ip in ip_list:
        print(f"\n\nConnecting to {ip}")
        out = send_show_commands(ip, "gandalf", "grey", com_list)
        pprint(out, width = 120)
#"show ap join stats summary all"
        #print(out)
        
