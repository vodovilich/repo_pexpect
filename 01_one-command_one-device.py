import pexpect
import sys


#pexpect defaults: 
# .expect returns 0 if matches the argument
# .expect reads until FIRST MATCH: if you send 2 commands without expect => before will find only 1st commmand output
# .sendline returns number of bytes send (1 symbol = 1 byte) + 1 byte for NEWLINE symbol
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

