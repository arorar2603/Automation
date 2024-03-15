import paramiko
import time
import shutil

def restart_up(Up_ip,username,password):
 client = paramiko.SSHClient()
 client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server
 client.connect(Up_ip, username=username, password=password)
 remote_conn = client.invoke_shell()

#Print terminal to screen
 output = remote_conn.recv(1000)
 remote_conn.send('\n')
 time.sleep(2)
 print(output)

#Enter into cli mode 
 remote_conn.send('cli\n')
 time.sleep(3)
 output = remote_conn.recv(1000)
 print(output)


#Restart command
 remote_conn.send('request system reboot both-routing-engines\n')
 time.sleep(3)
 output = remote_conn.recv(1000)
 print(output)

 remote_conn.send('yes\n')
 time.sleep(3)
 output = remote_conn.recv(1000)
 print(output)
 # Close the connection
 client.close()

 time.sleep(90)
 
 remote_conn.send('show system subscriber-management user-plane associations | refresh 5\n')
 time.sleep(90)
 output = remote_conn.recv(10000).decode()
 print(output)

 client.close()


def update_parameters_in_file(parameter_names, parameter_values, file_path_dest):
    # Open the file in read mode to read its content
    with open(file_path_dest, 'r') as file:
        lines = file.readlines()

    # Create a dictionary to store parameter names and their values
    parameters_dict = dict(zip(parameter_names, parameter_values))

    # Loop through the lines and replace parameter values if found
    for index, line in enumerate(lines):
        for parameter_name, parameter_value in parameters_dict.items():
            if parameter_name in line:
                lines[index] = line.replace(parameter_name, str(parameter_value))

    # Write the modified content back to the file
    with open(file_path_dest, 'w') as file:
        file.writelines(lines)

def create_and_update_userfile(filepath_src,file_name):
  shutil.copyfile(filepath_src,"User_Config_File /UP_CONFIG.txt" )
 
  parameter_names = ['Router_ip', 'Up_ip', 'Radius_ip']
  parameter_values = [10, 20, 30]
  file_path_dest = 'User Config File/'+file_name
  update_parameters_in_file(parameter_names, parameter_values, file_path_dest)


def uploadFiles(client,filepath_src,file_name):
   create_and_update_userfile(filepath_src,file_name)
   sftp_client    = client.open_sftp()
   config_file_git_path  = 'User Config files/'+file_name
   config_file_remote_path = file_name
   try:
     sftp_client.put(config_file_git_path, config_file_remote_path)
   except FileNotFoundError as err:
     print(f"File {config_file_git_path} was not found on the local system")
     
     
   sftp_client.close()  

def main(Up_ip):
   # Server credentials
   username = "root"
   password = "Embe1mpls"

# Create SSH client
   client = paramiko.SSHClient()
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server
   client.connect(Up_ip, username=username, password=password)


   file_name='UP_CONFIG.txt'
   filepath_src='Config_files/'+file_name
   uploadFiles(client,filepath_src,file_name)
   remote_conn = client.invoke_shell()

   #Print terminal to screen
   # output = remote_conn.recv(1000)
   remote_conn.send('\n')
   time.sleep(2)
   print(output)

   #Enter into cli mode 
   remote_conn.send('cli\n')
   time.sleep(3)
   output = remote_conn.recv(1000)
   print(output)

   #Enter configuration mode
   remote_conn.send('configure\n')
   time.sleep(2)
   output = remote_conn.recv(1000)
   print(output)


#Loading Config file for Cp 
   remote_conn.send('load set /var/tmp/'+file_name+'\n')
   time.sleep(15)
   output = remote_conn.recv(1000)
   print(output)

   remote_conn.send('commit\n')
   time.sleep(15)
   output = remote_conn.recv(1000)
   print(output)

# Close the connection
   client.close()
