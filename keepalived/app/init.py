#!/usr/bin/env python3
"""Keepalived Launcher"""
import netifaces
import ipaddress
import socket
import sys
import subprocess
from kubernetes import client, config

# gather config map input
vip_addr = '192.168.8.60'
router_id = '100'
vip_pass = 'SecretP4SS'

# find correct nic
search = ipaddress.ip_address(vip_addr)
for interface in netifaces.interfaces():
    nets = [ipaddress.ip_network(item['addr'] + '/' + item['netmask'], False)
            for item in netifaces.ifaddresses(interface).get(2, [])]
    vip_in_net = sum([search in net for net in nets]) > 0
    if vip_in_net:
        break
else:
    print('ERROR: Could not find an appropriate NIC for IP {}'.format(search_addr_in))
    sys.exit(1)

# get node order from k8s api
hostname = socket.gethostname()
config.load_incluster_config()
v1 = client.CoreV1Api()
for host_idx, host in enumerate(v1.list_node().items):
    if host.metadata.labels['kubernetes.io/hostname'] == hostname:
        break
else:
    print('ERROR: Unable to find hostname {} in cluster'.format(hostname))

# write the config file
with open('/tmp/keepalived.conf', 'w') as config:
    config.write(f"""global_defs {{
   router_id ocp_hosted_lb
   vrrp_skip_check_adv_addr
}}

vrrp_instance VI_1 {{
    state BACKUP
    interface {interface} # calculated
    virtual_router_id {router_id} # USER INPUT
    priority {100 - host_idx} # calculated
    advert_int 1
    authentication {{
        auth_type PASS
        auth_pass {vip_pass}  # USER INPUT
    }}
    virtual_ipaddress {{
        {vip_addr} # USER INPUT
    }}
}}""")
sys.stdout.write(f"""global_defs {{
   router_id ocp_hosted_lb
   vrrp_skip_check_adv_addr
}}

vrrp_instance VI_1 {{
    state BACKUP
    interface {interface} # calculated
    virtual_router_id {router_id} # USER INPUT
    priority {100 - host_idx} # calculated
    advert_int 1
    authentication {{
        auth_type PASS
        auth_pass {vip_pass}  # USER INPUT
    }}
    virtual_ipaddress {{
        {vip_addr} # USER INPUT
    }}
}}""")

# run keepalived
proc = subprocess.Popen(['keepalived', '-f', '/tmp/keepalived.conf', '-ln'])
sys.exit(proc.wait())