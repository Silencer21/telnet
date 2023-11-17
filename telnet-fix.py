#import modules
import pexpect
import difflib

def create_telnet_session(ip_address, username, password):
    try:
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
            print('-' * 3, 'FAILURE! entering username for: ', ip_address)
            exit()

        #session is expecting password, enter details
        session.sendline(password)
        result = session.expect(['#', pexpect.TIMEOUT])

        #check if error exists, if yes display and exit
        if result != 0:
            print('-' * 3, 'FAILURE! entering password for: ', ip_address)
            exit()

        # Login successful
        print('Login successful for: ', ip_address)

        #modify hostname
        session.sendline('config t')
        session.sendline('hostname R1')
        print('hostname modified for: ', ip_address)
        
        #display running config
        session.sendline('show running-config')
        result = session.expect(['#',pexpect.TIMEOUT])
        #check if error exists, if yes display and exit
        if result != 0:
            print('-' * 3, 'FAILURE! showing running-config for: ', ip_address)
            exit()

        #save file locally
        with open('running-config.txt','w') as file:
            file.write(session.before)

        print('file successfully saved locally')
        
        #display running-config
        session.sendline('show running-config')
        result = session.expect(['#',pexpect.TIMEOUT])
        
        #check for error
        if result != 0:
            print('-' * 3, 'FAILURE! displaying running-config for: ', ip_address)
            exit()
        #stores running-config    
        running_config = session.before

        #display startup-config
        session.sendline('show startup-config')
        result = session.expect(['#',pexpect.TIMEOUT])
        
        #check for error
        if result != 0:
            print('-' * 3, 'FAILURE! displaying startup-config for: ', ip_address)
            exit()
        
        #stores startup config 
        startup_config = session.before

        #compare configs
        if running_config == startup_config:
            print('running-config is the same as startup-config')
        else:
            print('running-config is different to startup-config')
            exit()
        
        #send running-config command
        session.sendline('show running-config')
        result = session.expect(['#',pexpect.TIMEOUT])

        #check for error
        if result != 0:
            print('-' * 3, 'FAILURE! displaying running-config for: ', ip_address)
            exit()

        #save running-config to file
        with open('running-config.txt','w') as file:
            file.write(session.before)

        #read from local offline running-config
        with open('running-config.txt','r') as file:
            local_config = file.readlines()

        
        #get current running config
        current_config = session.before.splitlines()

        #compare configs
        diff = difflib.unified_diff(current_config,local_config)
        
        #display differences
        for line in diff:
            print(line)


        # Close the session
        session.close()

    except Exception as e:
        print('Exception occurred:', str(e))

# define variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'

# create telnet session
create_telnet_session(ip_address, username, password)
