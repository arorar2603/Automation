
#Step 1 :Getting Input credentials from user 

# Server credentials
Router_ip = "10.205.59.12"
Up_ip= "10.205.53.169"
username = "root"
password = "Embe1mpls"




#Step 2: CUPS setup 


#Setting up UP 
import up
up.main(Up_ip)
# Note:Assuming docker already installed in your setup 
#setting up CP
import cp

#deactive bng Controller( Already added in config file while loading the config File )

# restart cp and up and check connectivity betwwen cp and up
# up.restart_up(Up_ip,username,password)
# cp.restart_cp(Router_ip,username,password)

# activate bng-controller subscribers group 


#Step 3


#free radius setup 
#
# import radius

# use test aaa command to verify setup working fine or not . 

# Setup Bng-Blaster 

