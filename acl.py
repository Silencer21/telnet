import pexpect

def configure_acl(device_ip: str, username: str, password: str, acl_rules: list):
    """
    Configures Access Control Lists (ACLs) on a network device to provide control over inbound and outbound network traffic.

    Parameters:
    - device_ip: str
        The IP address of the network device where ACLs will be configured.
    - username: str
        The username to authenticate with the network device.
    - password: str
        The password to authenticate with the network device.
    - acl_rules: list
        A list of ACL rules to be applied. Each rule should be a string in the format "<action> <source> <destination>".

    Returns:
    - bool:
        True if the ACL configuration was successful, False otherwise.
    """

    try:
        # Connect to the network device using SSH
        ssh_command = f"ssh {username}@{device_ip}"
        child = pexpect.spawn(ssh_command)

        # Wait for the password prompt and enter the password
        child.expect("password:")
        child.sendline(password)

        # Wait for the command prompt
        child.expect("#")

        # Configure ACLs
        for rule in acl_rules:
            # Send the ACL configuration command
            acl_command = f"access-list {rule}"
            child.sendline(acl_command)

            # Wait for the command to complete
            child.expect("#")

        # Save the configuration
        child.sendline("write memory")
        child.expect("#")

        # Close the SSH connection
        child.sendline("exit")
        child.expect(pexpect.EOF)

        return True

    except pexpect.ExceptionPexpect as e:
        print(f"Error configuring ACLs: {e}")
        return False

# Example usage:
device_ip = "192.168.1.1"
username = "admin"
password = "password"
acl_rules = [
    "permit 192.168.2.0/24 any",
    "deny any any"
]

result = configure_acl(device_ip, username, password, acl_rules)
if result:
    print("ACL configuration successful.")
else:
    print("ACL configuration failed.")
