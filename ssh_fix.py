

        # Perform further actions with the session if needed

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
