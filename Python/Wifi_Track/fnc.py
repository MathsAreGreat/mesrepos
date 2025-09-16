import subprocess


def check_device_connected(ip_range, mac_address=None, ip_address=None):
    # Run the `nmap` command to scan the network for active devices
    result = subprocess.run(['nmap', '-sn', ip_range], stdout=subprocess.PIPE)
    return result.stdout.decode()


# Example usage:
# Specify the network range and your son's device MAC or IP address here
network_range = "192.168.1.1/24"

nb = check_device_connected(network_range)
print(nb)
