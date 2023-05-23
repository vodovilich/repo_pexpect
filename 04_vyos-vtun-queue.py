import pexpect, sys, re, time
from pprint import pprint

def send_show_command(ip, command):
    with pexpect.spawn(f"ssh {ip}", timeout=10, encoding="utf-8") as ssh:
        ssh.expect("vyos@")
        ssh.expect("vyos@")
        ssh.sendline(command)
        ssh.expect("vyos@")

        output = ssh.before
        return output







if __name__ == "__main__":
    ip_list = ["101-vyos01", "201-vyos02", "301-vyos02"]
    for ip in ip_list:
        iflist = []
        print(f"\n\nCONNECTING TO {ip}")
        x = send_show_command(ip, 'show int')
        for str in x.split("\n"):
            if 'vtun' in str:
                print(str)
                print(str.split()[0])
                ifname = str.split()[0]
                iflist.append(ifname)
        print("\nInterfaces are going to be modified:")
        print(iflist)
        
        print(f"\n\nCONNECTING TO {ip} FOR EDITING:")
        """
        VYOS SPAWN behaviour: user mode - two expects after a command, and then - command-expect-before-expect
           USER mode: ssh -> expect-1 (before will show the banner) -> expect-2 (before will show prompt) -> command -> expect-1 (before will show output) -> expect-2 (before will show prompt)
           CONF mode: conf -> expect (before will show promt) -> command-expect-before - NO ADDITIONAL EXPECT NEEDED
                       command-expect-before, 
                       COMPARE-expect-before: SHOWS SHIT, 
                       COMMIT-expect-before: shows shit, but with OK at the end
                       SAVE-expect-before: shows saving
                       EXIT-expect-before: shows conf-prompt
                       ONE MORE expect-before: shows user-prompt
                       EXIT-expect-before: shows prompt
                       before: shows connection closet, expect: shows EOF
        """
        
        child = pexpect.spawn(f'ssh {ip}')
        child.expect("vyos@")
        child.expect("vyos@")
        child.sendline("conf")
        time.sleep(2)
        child.expect("vyos@")
        for vtun in iflist:
            child.sendline(f"set interfaces openvpn {vtun} openvpn-option \'txqueuelen 1000\'")   
            child.expect("vyos@")
            xx = child.before.decode('utf-8').splitlines()
            for line in xx:
                print(line)
            
            
        child.sendline("compare")
        time.sleep(2)
        child.expect("vyos@")
        xx = child.before.decode('utf-8').splitlines()
        for line in xx:
            print(line)
        
        child.sendline("commit")
        time.sleep(5)
        child.expect("vyos@")
        xx = child.before.decode('utf-8').splitlines()
        for line in xx:
            print(line)
        
        child.sendline("save")
        child.expect("vyos@")
        time.sleep(5)
        child.sendline("exit")
            


        
        
        
        