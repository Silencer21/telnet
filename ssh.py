#import modules

import pexpect

#define variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'


#create ssh session
session = pexpect.spawn('ssh ' + username + '@' + ip_address,encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

#check for error
if result != 0:
    print('--- FAILURE! creating session for: ',ip_address)
    exit()

#enter password
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

#check for error
if result != 0:
    print('--- FAILURE! entering password: ',password)
    exit()

#enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT,pexpect.EOF])

#check for errors
if result != 0:
    print('--- FAILURE! entering enable mode')
    exit()

#send enable password details
session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

#check for errors
if result != 0:
    print('--- FAILURE! entering enable mode after sending password')
    exit()

#enter config mode
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

#check for errors
if result != 0:
    print('--- FAILURE! entering config mode')
    exit()

#change hostname to R1
session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#',pexpect.TIMEOUT, pexpect.EOF])

#check for errors
if result != 0:
    print('--- FAILURE! setting hostname')
    exit()

#exit config mode
session.sendline('exit')

# Save the configuration to the local device
session.sendline('write memory')
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Check for errors and exit if needed
if result != 0:
    print('-' * 3, 'FAILURE! Saving the configuration')
    exit()
#exit enable mode
session.sendline('exit')

# Display a success message
print('-' * 25)
print('')
print('-' * 3, 'Success! Connecting to: ', ip_address)
print('-' * 3, 'Username: ', username)
print('-' * 3, 'Password: ', password)
print('-' * 25)
print('hostname changed to R1')
print('configuration saved')


# Terminate the SSH session
session.close()