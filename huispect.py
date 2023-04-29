import pexpect
import sys

print("pidor")

child = pexpect.spawn('ssh gandalf@192.168.100.27')
child.logfile = sys.stdout.buffer
child.expect('assword')
child.sendline('grey')
child.expect('#')
child.sendline('terminal length 0')
child.expect('#')
child.sendline('show ver')
child.expect('#')
x = child.before.decode('utf-8').splitlines()
child.sendline('exit')

for line in x:
    print(line)
