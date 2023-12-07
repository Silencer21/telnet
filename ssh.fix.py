import pexpect

def change_hostname(ip_address, username, password, enable_password, new_hostname):
    try:
        # Create an SSH connection
        session = pexpect.spawn(f'ssh -o "StrictHostKeyChecking=no" {username}@{ip_address}', encoding='utf-8', timeout=20)

        # Check for the password prompt
        session.expect('assword:')
        session.sendline(password)

        # Enter enable mode
        session.expect('>')
        session.sendline('enable')

        # Check for the enable password prompt
        session.expect('assword:')
        session.sendline(enable_password)

        # Enter config mode
        session.expect('#')
        session.sendline('configure terminal')

        # Change the hostname
        session.expect(r'\(config\)#')
        session.sendline(f'hostname {new_hostname}')

        # Save the configuration
        session.expect(r'{new_hostname}\(config\)#')
        session.sendline('write memory')

        # Exit config mode and enable mode
        session.expect('#')
        session.sendline('exit')
        session.expect('>')
        session.sendline('exit')

        # Display success message
        print('-' * 25)
        print('Success! Hostname change completed for:', ip_address)
        print('-' * 25)

    except pexpect.ExceptionPexpect as e:
        print('An error occurred:', str(e))

# Define variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
enable_password = 'class123!'
new_hostname = 'R1'

# Call the function to change hostname
change_hostname(ip_address, username, password, enable_password, new_hostname)
