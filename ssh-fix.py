import pexpect

# Define variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'
new_hostname = 'R1'

try:
    # Create an SSH connection
    session = pexpect.spawn('ssh -o "StrictHostKeyChecking 0" ' + username + '@' + ip_address, encoding='utf-8', timeout=20)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    # Check for errors and exit if needed
    if result != 0:
        print('-' * 3, 'FAILURE! Creating a session for:', ip_address)
        exit()

    # Provide the password
    session.sendline(password)
    result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

    # Check for errors and exit if needed
    if result != 0:
        print('-' * 3, 'FAILURE! Entering password:', password)
        exit()

    # Enter enable mode
    session.sendline('enable')
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    # Check for errors and exit if needed
    if result != 0:
        print('-' * 3, 'FAILURE! Entering enable mode')
        exit()

    # Send the enable password
    session.sendline(password_enable)
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

    # Check for errors and exit if needed
    if result != 0:
        print('-' * 3, 'FAILURE! Entering enable mode after sending the password')
        exit()

    # Enter config mode
    session.sendline('configure terminal')
    result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    # Check for errors and exit if needed
    if result != 0:
        print('-' * 3, 'FAILURE! Entering config mode')
        exit()

    # Change the hostname
    session.sendline('hostname ' + new_hostname)
    result = session.expect([r'{}\(config\)#'.format(new_hostname), pexpect.TIMEOUT, pexpect.EOF])

    # Check for errors and exit if needed
    if result != 0:
        print('-' * 3, 'FAILURE! Setting hostname')
        exit()

    # Save the configuration to the local device
    session.sendline('write memory')
    result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    # Check for errors and exit if needed
    if result != 0:
        print('-' * 3, 'FAILURE! Saving the configuration')

except Exception as e:
    print('-' * 3, 'SSH connection failed:', str(e))
