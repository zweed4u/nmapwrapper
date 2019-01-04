#!/usr/bin/python3
import socket
import subprocess


cidr_subnet_mask = 24

# assume something like: "default via 192.168.2.1 dev wlp2s0b1 proto dhcp metric 600" 
ip_route_proc = subprocess.Popen(['ip route | grep default | awk {\'print $3\'}'], stdout=subprocess.PIPE, shell=True)
gateway = ip_route_proc.communicate()[0].decode().strip()

nmap_proc = subprocess.Popen([f'sudo nmap -sn {gateway}/{cidr_subnet_mask}'], stdout=subprocess.PIPE, shell=True)
stdout = nmap_proc.communicate()[0].decode()

counter = 0
ips = []
macs = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_ip = s.getsockname()[0]
s.close()

for line in stdout.splitlines():
    if 'scan report for' in line.lower() and my_ip not in line.lower():
        ips.append(line.split('for ')[-1])
    if 'mac address' in line.lower():
        macs.append(line.split(': ')[-1].split(' ')[0])

assert len(ips) == len(macs)

for count in range(len(ips)):
    print(f'{ips[count]} - {macs[count]}')
