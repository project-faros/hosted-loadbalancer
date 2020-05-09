#!/usr/bin/env python3
"""Keepalived Launcher"""
import netifaces
import ipaddress
import os
import socket
import sys
import subprocess
from kubernetes import client, config

# contants
CONFIG_FILE = '/tmp/keepalived.conf'
PID_FILE = '/tmp/keepalived.pid'
VRRP_PID_FILE = '/tmp/keepalived.vrrp.pid'
CHECKERS_PID_FILE = '/tmp/keepalived.checkers.pid'

# gather config map input
vip_addr = os.environ.get('VIP_ADDR')
router_id = os.environ.get('ROUTER_ID')
vip_pass = os.environ.get('VIP_PASS')
fail = False
if not vip_addr:
    print('ERROR: The VIP_ADDR environment variable has not been set.')
    fail = True
if not router_id:
    print('ERROR: The ROUTER_ID environment variable has not been set.')
    fail = True
if not vip_pass:
    print('ERROR: The VIP_PASS environment variable has not been set.')
    fail = True
if fail:
    sys.exit(1)

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
with open(CONFIG_FILE, 'w') as config:
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
print(f"""global_defs {{
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
proc = subprocess.Popen(['keepalived', '-ln',
                         '-f', CONFIG_FILE,
                         '-p', PID_FILE,
                         '-r', VRRP_PID_FILE,
                         '-c', CHECKERS_PID_FILE])
sys.exit(proc.wait())
