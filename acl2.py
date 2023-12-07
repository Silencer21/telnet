import pexpect

# Define variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
hostname = 'R1'
crypto_map_name = 'MY_CRYPTO_MAP'
transform_set_name = 'MY_TRANSFORM_SET'
isakmp_key = 'cisco123!'

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
session.sendline('crypto isakmp policy 10')
session.sendline('authentication pre-share')
session.sendline(f'encryption aes')
session.sendline(f'hash sha')
session.sendline(f'group 2')
session.sendline(f'lifetime 3600')
session.expect('#')

session.sendline(f'crypto isakmp key {isakmp_key} address {ip_address}')

session.sendline(f'crypto ipsec transform-set {transform_set_name} esp-aes esp-sha-hmac')
session.sendline(f'crypto map {crypto_map_name} 10 ipsec-isakmp')
session.sendline(f'set peer {ip_address}')
session.sendline(f'set transform-set {transform_set_name}')
session.sendline(f'match address 101')

# Apply Crypto Map to Interface
session.sendline(f'interface GigabitEthernet0/0')
session.sendline(f'crypto map {crypto_map_name}')

# Show running config to confirm IPSec configuration
session.sendline('show running-config')
session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

if result != 0:
    print('-' * 3, 'FAILURE showing running configuration')
    exit()

# Saving to local file
with open('config.txt', 'w') as file:
    file.write(session.before)
print('Running configuration saved to config.txt')

# Terminate telnet session
session.sendline('quit')
session.close()
