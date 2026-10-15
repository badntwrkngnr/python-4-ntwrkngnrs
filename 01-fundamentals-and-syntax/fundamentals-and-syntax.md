# Module 01: Python Fundamentals and Syntax for Network Engineers

## Overview

Python has strict rules and community standards just like networking protocols (e.g., OSPF, BGP). This module covers core syntax, data types (`int`, `str`, `list`, `dict`), and style conventions tailored for network automation.

---

## Key Concepts & Networking Comparisons

### 1. Indentation Defines Code Blocks

* Unlike other programming languages that use curly braces `{ }`, Python uses **indentation** (4 spaces) to group blocks of code.
* *Network Analogy:* Think of how sub-commands under `interface GigabitEthernet0/0` or `router ospf 1` are indented in a Cisco IOS configuration.

### 2. Variables and Naming Rules

* A variable is a labeled container in memory (like a host-macro or alias).
* **The Common Network Engineer Mistake:** In CLI configs or DNS, we love hyphens (`core-rtr-01`). In Python, hyphens are interpreted as subtraction (`minus`). Always use **snake_case** with underscores (`core_rtr_01`).

| Element Type | Naming Convention | Network Example |
| :--- | :--- | :--- |
| **Variables / Functions** | `snake_case` | `router_hostname`, `get_bgp_status()` |
| **Constants** | `UPPER_SNAKE_CASE` | `DEFAULT_SSH_PORT = 22` |
| **Classes** | `PascalCase` | `CiscoIosSSH` |

### 3. Standard Input & Output (`print` and `input`)

* `print()` sends data to `stdout` (the terminal screen).
* `input()` pauses execution to capture `stdin` from the user.
* **Critical Rule:** Everything returned by `input()` is always a **String (`str`)**, even if the user types numbers (like a VLAN ID). You must explicitly convert types when doing mathematical or logical checks.

---

## Lab Exercise Example (`device_prompt.py`)

A basic script demonstrating variables, `input()`, and `print()` with a proper Linux shebang line:

```python
#!/usr/bin/env python

# Prompt the network engineer for device details
device_hostname = input("Enter the device hostname: ")
mgmt_ip_addr = input("Enter the management IP address: ")

# Print the collected information to standard output
print("-" * 40)
print(f"Target Device Hostname: {device_hostname}")
print(f"Target Management IP:   {mgmt_ip_addr}")
print(f"Data type of IP var:    {type(mgmt_ip_addr)}")
print("-" * 40)
```
