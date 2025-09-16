import json
import re
import subprocess
from time import sleep

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear


def check_device_connected(mac_address=None, ip_address=None):
    # Run the `nmap` command to scan the network for active devices
    # result = subprocess.run(['nmap', '-sn', ip_range], stdout=subprocess.PIPE)
    result = subprocess.run(
        ['ip', 'neigh'],
        stdout=subprocess.PIPE
    )
    output = result.stdout.decode()

    datas = [
        re.findall(
            r"(192.168.1.[0-9]+) .+ ([0-9a-z]{2}(:[0-9a-z]{2}){5})",
            e.lower()
        )
        for e in output.strip().split('\n')
        if "STALE" in e
    ]
    return [e[0][:2] for e in datas if e]


vv = 1
while True:
    nb = 0
    with open("infos.json", "r") as fl:
        data = json.load(fl)
    print(vv, ": Happy ?")
    for ip, mac in check_device_connected():
        print(data.get(mac.upper()))
        print(mac)
        print(ip)
        print()
        nb += 5
    sleep(2)
    print(upclear * (nb+1))
    vv += 1
