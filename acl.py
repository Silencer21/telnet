import pexpect
device_ip = "192.168.56.101"
username = "prne"
password = "cisco123!"
telnet_command = f"telnet {device_ip}"
telnet_session = pexpect.spawn(telnet_command)
telnet_session.expect("Username:")
telnet_session.sendline(username)
telnet_session.expect("Password:")
telnet_session.sendline(password)
telnet_session.expect("#")
telnet_session.sendline("configure terminal")
telnet_session.expect("#")

acl_name = "my_acl"
acl_rules = ["permit tcp any any eq 80", "deny ip any any"]

for rule in acl_rules:
    telnet_session.sendline(f"access-list {acl_name} {rule}")
    telnet_session.expect("#")
    interface_name = "GigabitEthernet0/1"
telnet_session.sendline(f"interface {interface_name}")
telnet_session.expect("#")
telnet_session.sendline(f"ip access-group {acl_name} in")
telnet_session.expect("#")
telnet_session.sendline("end")
telnet_session.expect("#")
telnet_session.sendline("write memory")
telnet_session.expect("#")
telnet_session.sendline("exit")
