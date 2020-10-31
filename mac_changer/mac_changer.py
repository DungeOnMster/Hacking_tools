#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="The new MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing Mac Address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    mac_address_search_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_res:
        return mac_address_search_res.group(0)
    else:
        print("No mac address found for the given interface, Please enter a valid interface.")


changed = get_arguments()
current_mac = get_current_mac(changed.interface)
print("Current MAC:" + str(current_mac))
change_mac(changed.interface, changed.new_mac)

current_mac = get_current_mac(changed.interface)
if current_mac == changed.new_mac:
    print("[+] MAC Address was successfully changed to " + current_mac)
else:
    print("[-] MAC Address did not change")