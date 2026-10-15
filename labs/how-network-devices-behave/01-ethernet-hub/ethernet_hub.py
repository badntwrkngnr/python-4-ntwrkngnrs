hubports = [
    "Ethernet0/0",
    "Ethernet0/1",
    "Ethernet0/2",
    "Ethernet0/3"
]

boot_message = """
PythonHub is booting ...
Please wait
"""
print(boot_message)
print(hubports[0])
print(hubports[1])
print(hubports[2])
print(hubports[3])
while True:
    port = input("Generate signal into port: ")
    try:
        port_number = int(port)
    except ValueError:
        # Non-numeric input (e.g. "abc" or an empty line) is also invalid
        port_number = -1
    if port_number < len(hubports) and port_number >= 0:
        ingress_port = hubports[port_number]
        print("⚡️ Receiving signal on " + ingress_port)
    else:
        print("❌ Invalid entry: " + port)
        break

    for egress_port in hubports:
        if egress_port == ingress_port:
            print("🔴 NOT transmitting on port " + egress_port)
        else:
            print("🟢 Transmitting on port " + egress_port)
