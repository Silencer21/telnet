import pexpect

# Define variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
hostname = 'R1'

# Create telnet session
session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8', timeout=20)
result = session.expect(['Username:', pexpect.TIMEOUT])

# Check if error exists, if yes display and exit
if result != 0:
    print('-' * 3, 'FAILURE! creating session for: ', ip_address)
    exit()

# Session is expecting username, enter details
session.sendline(username)
result = session.expect(['Password: ', pexpect.TIMEOUT])

# Check if error exists, if yes display and exit
if result != 0:
    print('-' * 3, 'FAILURE! entering username: ', username)
    exit()

# Session is expecting password, enter details
session.sendline(password)
result = session.expect(['#', pexpect.TIMEOUT])

# Check if error exists, if yes display and exit
if result != 0:
    print('-' * 3, 'FAILURE! entering password: ', password)
    exit()

# Display success message
print('-' * 25)
print('')
print('-' * 3, 'Success connecting to: ', ip_address)
print('-' * 3, 'Username: ', username)
print('-' * 3, 'Password: ', password)
print('')
print('-' * 25)

# Modify hostname
session.sendline('configure terminal')
result = session.expect(([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF]))

if result != 0:
    print('-' * 3, 'FAILURE entering config mode')
    exit()

session.sendline('hostname ' + hostname)
result = session.expect(([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF]))
if result != 0:
    print('-' * 3, 'FAILURE setting hostname')
    exit()

result = session.expect(([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF]))
print('Hostname changed to: ', hostname)

# Configure IPSec
session.sendline('crypto isakmp policy 1')
result = session.expect(([r'\(config-isakmp\)#', pexpect.TIMEOUT, pexpect.EOF]))
if result != 0:
    print('-' * 3, 'FAILURE configuring ISAKMP policy')
    exit()

session.sendline('encryption aes 256')
result = session.expect(([r'\(config-isakmp\)#', pexpect.TIMEOUT, pexpect.EOF]))
if result != 0:
    print('-' * 3, 'FAILURE setting encryption for ISAKMP policy')
    exit()

session.sendline('hash sha256')
result = session.expect(([r'\(config-isakmp\)#', pexpect.TIMEOUT, pexpect.EOF]))
if result != 0:
    print('-' * 3, 'FAILURE setting hash for ISAKMP policy')
    exit()

session.sendline('exit')
result = session.expect(([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF]))
if result != 0:
    print('-' * 3, 'FAILURE exiting from IPSec configuration mode')
    exit()

session.sendline('crypto ipsec transform-set myset esp-aes 256 esp-sha256-hmac')
result = session.expect(([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF]))


session.sendline('exit')
result = session.expect(([r'#', pexpect.TIMEOUT, pexpect.EOF]))
if result != 0:
    print('-' * 3, 'FAILURE exiting from config mode')
    exit()

# Show IPsec configuration
session.sendline('show crypto isakmp policy')
result = session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('-' * 3, 'FAILURE showing ISAKMP policy')
    exit()

session.sendline('show crypto isakmp sa')
result = session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('-' * 3, 'FAILURE showing ISAKMP SA')
    exit()

session.sendline('show crypto ipsec transform-set')
result = session.expect([r'#', pexpect.TIMEOUT, pexpect.EOF])
if result != 0:
    print('-' * 3, 'FAILURE showing IPsec transform-set')
    exit()

# Save running configuration to file
with open('config.txt','w') as file:
    file.write(session.before)
    print('successfully implemented IPSec')
# Terminate telnet session
session.sendline('quit')
session.close()
