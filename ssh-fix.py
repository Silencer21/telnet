
import pexpect
import difflib


# Define variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'
save_running = 'running_config.txt'
save_startup = 'startup_config.txt'

# Create the SSH session
session = pexpect.spawn('ssh ' + username + '@' + ip_address,
encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])


# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit()

# Session expecting password, enter details
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering password: ', password)
    exit()


# Enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! entering enable mode')
    exit()
# Send enable password details
session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! entering enable mode after sending password')
    exit()


# Enter configuration mode
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! entering config mode')
    exit()


# Change the hostname to R1
session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
    print('--- Failure! setting hostname')

# Show running-config
session.sendline('exit')
session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
session.sendline('terminal length 0')
session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
session.sendline('show running-config')
session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# saving the file locally
with open(save_running, 'w') as file:
    file.write(session.before)

#Show startup-config
session.sendline('show startup-config')
session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Saving the startup file locally
with open(save_startup, 'w') as file :
    file.write(session.before)

running_file = open(save_running, 'r')
running_data = running_file.readlines()

startup_file = open(save_startup, 'r')
startup_data = startup_file.readlines()


diff = difflib.ndiff(running_data, startup_data)
#diffs_file = 'diffs_file.txt'
for diffs in diff:
    print(diffs)
 # with open (diffs_file, 'a') as file:
  #
  #       file.write(diffs)

# Exit config mode
session.sendline('exit')
# Exit enable mode
session.sendline('exit')

print('-------------------------------------------------------------------------')
print('')
print('--- You have logged in succesfully! connecting to:', ip_address)
print('---                                      Username: ' , username)
print('---                                      Password: ' , password)
print('')
print('-------------------------------------------------------------------------')

# Terminate SSH session
session.close()
