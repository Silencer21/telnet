#import modules
import pexpect

#define variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'

#create telnet session
session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8',timeout=20)
result = session.expect(['Username:',pexpect.TIMEOUT])

#check if error exists,if yes display and exit
if result != 0:
    print('-'*3, 'FAILURE! creating session for: ',ip_address)
    exit()

#session is expecting username, enter details
session.sendline(username)
result = session.expect(['Password: ',pexpect.TIMEOUT])

##check if error exists,if yes display and exit
if result != 0:
    print('-'*3, 'FAILURE! entering username: ',username)
    exit()

#session is expecting password,enter details
session.sendline(password)
result = session.expect(['#',pexpect.TIMEOUT])

#check if error exists,if yes display and exit
if result != 0:
    print('-'*3, 'FAILURE! entering password: ',password)
    exit()

#display success message

print('-'*25)
print('')
print('-'*3, 'Success connecting to: ',ip_address)
print('-'*3,              'Username: ',username)
print('-'*3,              'Password: ', password)
print('')
print('-'*25)

#modify hostname
session.sendline('configure terminal')
result = session.expect(([r'\(config\)#',pexpect.TIMEOUT,pexpect.EOF]))

if result != 0:
    print('-'*3,'FAILURE entering config mode')
    exit()
hostname = 'R1'
session.sendline('hostname ' + hostname)
result = session.expect(([r'\(config\)#',pexpect.TIMEOUT,pexpect.EOF]))
if result != 0:
    print('-'*3,'FAILURE setting hostname')
    exit()
result = session.expect(([r'\(config\)#',pexpect.TIMEOUT,pexpect.EOF]))
print('Hostname changed to: ',hostname)

#show running config
session.sendline('show running-config')
result = session.expect(['#',pexpect.TIMEOUT,pexpect.EOF])

if result != 0:
    print('-'*3,'FAILURE showing running configuration')
    exit()

#saving to local file 
with open('config.txt','w') as file:
    file.write(session.before)
print('running configuration saved to config.txt')


session.expect('R1\(config\)#')
#configure loopback address
session.sendline('int loopback0')
session.expect('R1\(config\)#')
session.sendline('ip addr 10.0.0.1 255.255.255.255')
session.expect('R1\(config\)#')

#configure another interface
session.sendline('int g0/02')
session.expect('R1\(config\)#')
session.sendline('int g 2')
session.expect('R1\(config\)#')
session.sendline('ip addr 192.168.2.1 255.255.255.0')
session.expect('R1\(config\)#')

#exit config mode and save 
session.sendline('end')
session.expect('R1#')
session.sendline('write memory')

#configuring rip
session.sendline('conf t')
session.expect('R1\(config\)#')
session.sendline('router rip')
session.expect('R1\(config-router\)#')
session.sendline('network 192.168.56.0')
session.expect('R1\(config-router\)#')
print('router interface configured successfully')

#save and exit
session.sendline('end')
session.expect('R1#')
session.sendline('write memory')

#terminate telnet session
session.sendline('quit')
session.close()
