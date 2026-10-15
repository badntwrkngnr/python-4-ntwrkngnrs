from netmiko import ConnectHandler

switches = ["sw1", "sw2"]

comandos = [
    "vlan 10",
    "name LAB",
    "interface Ethernet2",
    "switchport mode access",
    "switchport access vlan 10",
    "interface Ethernet1",
    "switchport mode trunk",
    "switchport trunk allowed vlan 10",
]

for nome in switches:
    device = {
        "device_type": "arista_eos",
        "host": nome,
        "username": "admin",
        "password": "admin",
    }

    print(f"--- conectando em {nome} ---")
    conexao = ConnectHandler(**device)
    conexao.enable()
    saida = conexao.send_config_set(comandos)
    print(saida)
    conexao.disconnect()