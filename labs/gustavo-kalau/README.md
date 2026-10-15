# Lab: Do CLI ao Código (Gustavo Kalau)

> **Source:** practice code written while following the series [**Do CLI ao Código**](https://gustavokalau.com.br/do-cli-ao-codigo/) by Gustavo Kalau. Credit for the concepts, structure and teaching approach belongs to the author. This folder holds only my own practice code and notes; for the original content, follow the series.

The series goes from the command line to the first Python scripts for network automation. Each lab here pairs a [containerlab](https://containerlab.dev/) topology with the code that automates it.

| Lab | Topology | Code | Status |
| :--- | :--- | :--- | :--- |
| [`lab01`](lab01/) | 2 Arista cEOS switches + 2 Linux hosts, trunk between the switches | [`config_vlan.py`](lab01/config_vlan.py) — Netmiko pushes a VLAN and port config | Done |
| [`lab02`](lab02/) | `cisco-lab`: 2 Cisco IOL routers, 2 Cisco IOL L2 switches, 2 Linux hosts in different subnets | none yet | Topology only |

## Lab 01 — VLAN configuration with Netmiko

```text
pc1 ── sw1 ══ sw2 ── pc2
        trunk
```

| Link | Purpose |
| :--- | :--- |
| `sw1:eth1` ↔ `sw2:eth1` | trunk between the switches |
| `pc1:eth1` ↔ `sw1:eth2` | host 1 (`192.168.10.11/24`) |
| `pc2:eth1` ↔ `sw2:eth2` | host 2 (`192.168.10.12/24`) |

`config_vlan.py` loops over `sw1` and `sw2`, connects with Netmiko (`arista_eos`), enters enable mode and sends one configuration set per switch:

- creates VLAN 10 named `LAB`;
- `Ethernet2`: access port in VLAN 10 (towards the host);
- `Ethernet1`: trunk allowing VLAN 10 (towards the other switch).

## Lab 02 — `cisco-lab` topology

| Node | Kind | Role |
| :--- | :--- | :--- |
| `r1`, `r2` | Cisco IOL (L3) | routers, linked to each other (`r1:eth1` ↔ `r2:eth1`) |
| `sw1`, `sw2` | Cisco IOL (L2) | access switches: `sw1:eth1` ↔ `r1:eth2` and `sw1:eth2` ↔ `pc1:eth1` (same pattern for `sw2`, `r2`, `pc2`) |
| `pc1` | Linux | `192.168.0.13/24`, static route to `192.168.1.0/24` via `192.168.0.1` |
| `pc2` | Linux | `192.168.1.13/24`, static route to `192.168.0.0/24` via `192.168.1.1` |

Only the topology file exists so far; the automation code for this lab has not been written yet.

## Prerequisites

| You need | Where it comes from |
| :--- | :--- |
| Lists, `for` loops, variables, running scripts | [Guides 01–03](../../README.md#learning-path) |
| Dictionaries, f-strings and `**` argument unpacking (used to build the Netmiko connection) | not covered in the guides yet |
| Netmiko (see the [Week 1 guide](../../01-fundamentals-and-syntax/guide.md) for what it does) | `requirements.txt` in this folder |
| Docker and containerlab | installed on the machine that runs the labs |
| Router/switch images | **not included**: import the Arista cEOS image as `ceos:4.36.2.f` and build the Cisco IOL images locally (for example with [hellt/vrnetlab](https://github.com/hellt/vrnetlab)) |

## How to run (lab 01)

Activate your virtual environment first (see the [main README](../../README.md#setup)), then:

```bash
cd labs/gustavo-kalau
python -m pip install -r requirements.txt

sudo containerlab deploy -t lab01/lab01.clab.yml
python lab01/config_vlan.py          # run it on the machine where the lab is deployed
sudo containerlab destroy -t lab01/lab01.clab.yml
```

The script reaches the switches by node name (`sw1`, `sw2`). With `prefix: ""` in the topology, container names match node names.

To check the result, run `show vlan` on the switches and `docker exec pc1 ping -c 3 192.168.10.12`.

## Notes

- **Credentials:** `config_vlan.py` keeps the lab credentials inline for simplicity. That is acceptable in a disposable lab and nowhere else; moving them to environment variables or SSH keys is the natural first refactor.
- **`requirements.txt`** is a full `pip freeze` from the practice repository, so it includes transitive dependencies. It also lists `ntc_templates` and `textfsm` for parsing `show` output, which the scripts do not use yet.
- **`*.annotations.json`** only store node positions for the containerlab VS Code extension. They can be ignored.
