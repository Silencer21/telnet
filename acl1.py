#import modules
import pexpect

#define variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'

#create telnet session
session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Username:', pexpect.TIMEOUT])

#check if error exists, if yes display and exit
if result != 0:
    print('-' * 3, 'FAILURE! creating session for: ', ip_address)
    exit()

#session is expecting username, enter details
session.sendline(username)
result = session.expect(['Password: ', pexpect.TIMEOUT])

#check if error exists, if yes display and exit
if result != 0:
    print('-' * 3, 'FAILURE! entering username: ', username)
    exit()

#session is expecting password, enter details
session.sendline(password)
result = session.expect(['#', pexpect.TIMEOUT])

#check if error exists, if yes display and exit
if result != 0:
    print('-' * 3, 'FAILURE! entering password: ', password)
    exit()

#display success message
print('-' * 25)
print('')
print('-' * 3, 'Success connecting to: ', ip_address)
print('-' * 3, 'Username: ', username)
print('-' * 3, 'Password: ', password)
print('')
print('-' * 25)

#modify hostname
session.sendline('configure terminal')
result = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('-' * 3, 'FAILURE entering config mode')
    exit()
hostname = 'R1'
session.sendline(f'hostname {hostname}')
result = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('-' * 3, 'FAILURE setting hostname')
    exit()
result = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
print('Hostname changed to: ', hostname)

#configure ACLs
session.sendline('ip access-list extended BLOCK_TRAFFIC')
session.expect([r'\(config-ext-nacl\)#', pexpect.TIMEOUT, pexpect.EOF])
session.sendline('deny ip any any')
session.expect([r'\(config-ext-nacl\)#', pexpect.TIMEOUT, pexpect.EOF])
session.sendline('exit')

#apply ACL to interface
session.sendline('interface Ethernet0/0')  # Replace with the appropriate interface
session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
session.sendline('ip access-group BLOCK_TRAFFIC in')
session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
session.sendline('exit')

#save the configuration
with open('config.txt','w') as file:
    file.write(session.before)
    print('running configuration saved to config.txt')

print('ACLs configured successfully!')
#terminate telnet session
session.sendline('quit')
session.close()
