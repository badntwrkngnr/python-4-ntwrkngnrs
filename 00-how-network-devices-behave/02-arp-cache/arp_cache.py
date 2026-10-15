hosts = {
    "172.16.0.1": "00:11:22:33:44:55",
    "172.16.0.31": "DE:AD:BE:EF:00:03",
    "172.16.0.32": "12:34:56:78:9A:04",
    "172.16.0.33": "C0:FF:EE:00:00:05",
    "172.16.0.148": "AA:BB:CC:DD:EE:02",
    "172.16.0.149": "99:88:77:66:55:06"
}

print("Welcome to PythonArpCache!")
ip_addr = input("Which IP address to look up? ")

mac_addr = hosts.get(ip_addr)

if mac_addr:
    print(f"The host IP address {ip_addr} maps to MAC address {mac_addr}")
else:
    print(f"The host IP address {ip_addr} is not found")
    hosts[ip_addr] = "Incomplete       "

    print("! show ip arp")
    print("Protocol  Hardware Addr      Type  Address")
    for cached_ip, cached_mac in hosts.items():
        print(f"Internet  {cached_mac}  ARPA  {cached_ip}")