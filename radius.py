import paramiko

def configure_freeradius_via_ssh(router_ip, username, password, clients_config, users_config):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()

        # Automatically add the server's host key (this is insecure, better ways to do it in production)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the FreeRADIUS server
        ssh.connect(router_ip, username=username, password=password, timeout=10)

        # Configure clients.conf
        with ssh.open_sftp() as sftp:
            with sftp.file('/etc/freeradius/3.0/clients.conf', 'w') as file:
                file.write(clients_config)

        # Configure users
        with ssh.open_sftp() as sftp:
            with sftp.file('/etc/freeradius/3.0/users', 'w') as file:
                file.write(users_config)

        # Restart FreeRADIUS server
        stdin, stdout, stderr = ssh.exec_command('systemctl restart freeradius')

        # Print the output of the restart command
        print("Restart Command Output:")
        print(stdout.read().decode())

        print("FreeRADIUS configuration updated and server restarted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the SSH connection
        if ssh:
            ssh.close()

# Replace these values with your FreeRADIUS server details
router_ip = '10.206.213.189'
username = 'root'
password = 'Embe1mpls'

# Replace these configurations with your desired clients and users configurations
clients_configuration = """
client test-client {
  ipaddr = 10.206.214.158
  secret = joshua
}
"""

users_configuration = """
DEFAULTUSER Cleartext-Password := "joshua"
"""

# Configure FreeRADIUS and restart the server via SSH
configure_freeradius_via_ssh(router_ip, username, password, clients_configuration, users_configuration)
