#!/usr/bin/env python

import scapy.all as scapy
import subprocess
import argparse
import re


def get_args():
    x = argparse.ArgumentParser()
    x.add_argument("-t", "--target", dest="ip_range", help="Give the IP address range to be scanned")
    options = x.parse_args()
    if not options.ip_range:
        x.error("[-] Please specify an IP range")
    return options


def scan(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    ans_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for each_element in ans_list:
        clients_dict = {"ip": each_element[1].psrc, "mac": each_element[1].hwsrc}
        clients_list.append(clients_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n-------------------------------------------------------")
    for each_element in results_list:
        print(each_element["ip"] + "\t\t" + each_element["mac"])

options = get_args()
scan_result = scan(options.ip_range)
print_result(scan_result)