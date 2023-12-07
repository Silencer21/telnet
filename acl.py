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
