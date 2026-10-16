---
title: "Week 4 — Sets, Dictionaries and Exceptions"
source: "Study notes based on Kirk Byers, Learning Python for Network Engineers (Lesson 4)"
status: needs-review
---

# Week 4 Study Guide: Sets, Dictionaries, and Exception Handling for Network Automation

**Course:** Learning Python for Network Engineers (Kirk Byers)  
**Target Level:** English B1/B2  
**Focus:** Treating the Network as a System through Data Modeling, State Auditing, and Resilient Automation

## 1. Executive Summary: Why Week 4 Changes How You Automate Networks

When you start learning Python, you usually write scripts like a checklist of CLI commands: connect to a router, run a command, and print the text output. However, when you **treat the network as a system**, you stop thinking about raw text and start thinking about **structured state** and **system reliability**.

Week 4 introduces the three core pillars that allow you to model and protect a network system in code:

1. **Sets (`set`) — Auditing Network State and Comparing Topologies:** A network is full of collections that must be unique, such as active VLANs on a trunk, IP addresses in an IPAM subnet, or BGP peers. Sets automatically remove duplicates and let you compare two network states (for example, finding duplicate IP addresses between two data centers or checking which VLANs are missing from a switch) using single-line mathematical operations.
2. **Dictionaries (`dict`) — Modeling Devices, Interfaces, and API Payloads:** Together with lists, dictionaries are the most important data structure in Python. Modern network automation tools (Netmiko, NAPALM, Nornir, Ansible, RESTCONF, and NX-API) represent network devices and interfaces as key-value pairs and nested dictionaries. Dictionaries also give you near-instant `O(1)` lookup speed, even if you are searching through 100,000 MAC addresses or BGP routes.
3. **Exception Handling (`try` / `except` / `finally`) — Building Resilient Automation:** Real networks are imperfect. Devices lose power, TACACS+ credentials fail, firewalls block SSH ports, and CLI outputs change across OS versions. Without exception handling, a single unreachable switch will crash your script and stop a 100-device maintenance job. Exception handling lets your script catch expected failures, log the problem, clean up sessions safely, and continue running—or intentionally fail fast when the system state is unsafe.

## 2. Sets: Managing Unique Network Elements and State Audits

### 2.1 What is a Set?

A **set** is an **unordered collection of unique elements**.

* **Unique elements:** A set can only store one copy of each item. If you add duplicate items (such as the same IP address twice), Python automatically removes the duplicates.
* **Unordered (No indices):** Unlike lists, sets do not keep elements in a specific order. Because there is no order, you **cannot** access items by index (for example, `my_set[0]` will raise a `TypeError`).
* **Syntax:** You define a set using curly braces `{}` with elements separated by commas. *(Note: To create an empty set, you must use `set()`, because empty curly braces `{}` create an empty dictionary.)*

```python
# Creating a set of IP addresses (notice '192.168.100.1' is listed twice)
ip_addresses = {
    "192.168.100.1",
    "192.168.100.2",
    "192.168.100.3",
    "192.168.100.1",  # Duplicate entry
}

print(type(ip_addresses))
# Output: <class 'set'>

print(ip_addresses)
# Output: {'192.168.100.1', '192.168.100.2', '192.168.100.3'}
# The duplicate '192.168.100.1' was automatically removed!
```

### 2.2 Modifying Sets (Sets are Mutable)

Sets are **mutable**, meaning you can add or remove elements in-place without creating a new set in memory.

| Method / Operation | Behavior | Raises an Error if Item is Missing/Present? | Network Automation Use Case |
| :--- | :--- | :--- | :--- |
| `my_set.add(elem)` | Adds a single element to the existing set. | No (if already present, it simply does nothing). | Adding a newly discovered neighbor IP to a set of visited devices. |
| `my_set.update(other_set)` | Adds multiple elements from another set or list into the existing set in-place, removing duplicates. | No. | Merging a list of newly provisioned VLANs into an existing switch VLAN set. |
| `my_set.remove(elem)` | Removes a specific element from the set. | **Yes (`KeyError`)** if the element does not exist in the set. | Removing an IP when you want the script to alert you if the IP was already missing. |
| `my_set.discard(elem)` | Removes a specific element from the set if it is present. | **No** (completes silently even if you run it multiple times). | Safely ensuring a deprecated VLAN (like VLAN 1 or a legacy voice VLAN) is removed without crashing. |

```python
addresses = {"192.168.100.1", "192.168.100.2", "192.168.100.3"}

# 1. Add a single IP address
addresses.add("10.1.1.1")

# 2. Update the set with multiple IPs (one overlaps, one is new)
addresses.update({"10.1.1.1", "10.1.1.2"})
# 'addresses' now contains 5 unique IPs

# 3. Remove an IP strictly (.remove raises KeyError if missing)
addresses.remove("10.1.1.1")

# 4. Remove an IP safely (.discard never raises an error)
addresses.discard("10.1.1.1")  # Already removed, but no error happens!
```

### 2.3 Set Operations: Comparing Network States

Set operations are where sets become a superpower for network engineers. Imagine you have two sets of IP addresses—one from your **San Francisco (`sf_addresses`)** router and one from your **Los Angeles (`la_addresses`)** router—and someone accidentally configured `10.1.1.1` in both locations:

```python
sf_addresses = {"192.168.100.1", "192.168.100.2", "192.168.100.3", "10.1.1.1"}
la_addresses = {"10.1.1.1", "10.220.33.1", "10.220.33.2"}
```

None of the operators below modify `sf_addresses` or `la_addresses`; instead, they return a **new set** that you can save into a variable.

| Operation | Operator | Equivalent Method | What It Returns | Network Engineering Scenario |
| :--- | :--- | :--- | :--- | :--- |
| **Union** | `set_a \| set_b` | `set_a.union(set_b)` | All unique elements combined from both sets (duplicates appear only once). | Building a complete master list of all IP addresses or VLANs used across both SF and LA sites. |
| **Intersection** | `set_a & set_b` | `set_a.intersection(set_b)` | Only elements that exist in **both** sets (common/overlapping items). | Finding duplicate IP conflicts (`{'10.1.1.1'}`) between two sites, or finding VLANs allowed on **all** trunk ports. |
| **Symmetric Difference** | `set_a ^ set_b` | `set_a.symmetric_difference(set_b)` | Elements that are in either set, **excluding** any overlapping elements. | Finding all non-conflicting IPs, or identifying configuration drift (VLANs configured on Switch A or Switch B, but not both). |
| **Subtraction (Difference)** | `set_a - set_b` | `set_a.difference(set_b)` | Elements in the first set after removing any elements that also appear in the second set (**order matters!**). | `sf_addresses - la_addresses` gives IPs exclusively in SF. `la_addresses - sf_addresses` gives IPs exclusively in LA. |
| **Subset / Disjoint Checks** *(Additional Reading)* | `<=` / `.isdisjoint()` | `set_a.issubset(set_b)` / `set_a.isdisjoint(set_b)` | Returns `True` or `False`. | Checking if a trunk port's VLANs are a valid subset of the switch database (`issubset`), or verifying two VRFs share zero overlapping subnets (`isdisjoint`). |

```python
# Union: All unique IPs across both data centers
all_ips = sf_addresses | la_addresses
# {'192.168.100.1', '192.168.100.2', '192.168.100.3', '10.1.1.1', '10.220.33.1', '10.220.33.2'}

# Intersection: Find the duplicate IP conflict!
conflicting_ips = sf_addresses & la_addresses
# {'10.1.1.1'}

# Symmetric Difference: All IPs EXCEPT the overlapping '10.1.1.1'
non_overlapping_ips = sf_addresses ^ la_addresses
# {'192.168.100.1', '192.168.100.2', '192.168.100.3', '10.220.33.1', '10.220.33.2'}

# Subtraction (Order matters!)
only_in_sf = sf_addresses - la_addresses
# {'192.168.100.1', '192.168.100.2', '192.168.100.3'}

only_in_la = la_addresses - sf_addresses
# {'10.220.33.1', '10.220.33.2'}
```

### 2.4 Set Comprehensions (*Optional / Intermediate Content*)

A **set comprehension** lets you dynamically build a set in a single concise expression using a `for` loop. The syntax is identical to a list comprehension, except you use **curly braces `{}`** instead of square brackets `[]`.

```python
# 1. Basic Set Comprehension
my_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
squares = {x**2 for x in my_set}

# 2. Set Comprehension with a Conditional Filter (only even numbers)
even_squares = {x**2 for x in my_set if x % 2 == 0}
# Output: {0, 4, 16, 36, 64}

# 3. Multiple For Loops and a Conditional (formatted across multiple lines for readability)
# Read multiple loops from top to bottom (or left to right):
# Outer loop: x goes from 0 to 4. Inner loop: y goes from 1 to 9.
matching_octets = {
    f"{x}.{y}"
    for x in range(5)
    for y in range(1, 10)
    if x == y
}
# Output: {'1.1', '2.2', '3.3', '4.4'}
```

**Network Engineering Example:** Extracting a unique set of active uplink interface names from a raw list of interface records:

```python
raw_interfaces = ["Gi0/1", "Gi0/2", "Gi0/1", "Vlan1", "Lo0", "Gi0/3"]
gigabit_ports = {intf for intf in raw_interfaces if intf.startswith("Gi")}
# Output: {'Gi0/1', 'Gi0/2', 'Gi0/3'} (automatically deduplicated and filtered!)
```

## 3. Dictionaries: Modeling Network Devices, Interfaces, and State

### 3.1 Dictionary Basics and `O(1)` Lookup Performance

A **dictionary** is a collection of **key-value pairs** (`key: value`). In other programming languages, dictionaries are often called *hashes*, *hash maps*, or *associative arrays*.

* **Insertion Order Preserved (Python 3.7+):** Dictionaries remember the exact order in which keys were inserted. If you add `router1`, then `router2`, then `router3`, looping over the dictionary will always return them in that exact order.
* **Keys and Values:** Keys must be unique and immutable—in network automation, keys are almost always **strings** (like `'router1'` or `'GigabitEthernet0/0/0'`) or **integers** (like VLAN ID `10`). Values can be any data type: a string, an integer, a Boolean, a list, a set, or another dictionary.
* **Fast `O(1)` Lookup Time (Big-O Notation):** In computer science, dictionary key lookups are **`O(1)` (constant time)**. Whether your dictionary has 10 routers or 100 million BGP prefixes, looking up a value by its key takes virtually the exact same, near-instant amount of time. Lists require scanning element by element (`O(n)`), whereas dictionaries jump straight to the key in memory.

```python
# Creating a dictionary mapping device hostnames to management IP addresses
routers = {
    "router1": "10.1.1.1",
    "router2": "10.1.1.2",
    "router3": "10.1.1.3",
}

# Accessing a value using its key in square brackets
print(routers["router1"])  # Output: 10.1.1.1

# Updating an existing key or assigning a new key-value pair
routers["router1"] = "10.1.1.99"
routers["router4"] = "10.1.1.4"
```

### 3.2 Handling Missing Keys: `KeyError` vs. `.get()`

If you try to access a key that does not exist using square brackets (`routers["router5"]`), Python raises a **`KeyError` exception** and crashes your script.

When polling network devices or parsing API responses where optional fields might be missing (such as an interface description or secondary IP), use the **`.get()` method** for graceful lookups:

* `routers.get("router5")` returns `None` if the key does not exist (no exception is raised).
* `routers.get("router5", "unknown")` returns your custom default value (`"unknown"`) if the key does not exist.

```python
# Safe lookup with default None
ip = routers.get("router5")
print(ip)  # Output: None

# Safe lookup with custom fallback string
ip_status = routers.get("router5", "No Management IP Assigned")
print(ip_status)  # Output: No Management IP Assigned
```

### 3.3 Looping Over Dictionaries (`.keys()`, `.values()`, `.items()`)

When you iterate over a dictionary, you have three clean patterns depending on what data you need:

```python
# 1. Default loop: Iterates over KEYS (in insertion order)
for hostname in routers:
    print(hostname)

# 2. .values(): Iterates over VALUES only (in insertion order)
for ip_addr in routers.values():
    print(ip_addr)

# 3. .items(): Iterates over BOTH keys and values using tuple unpacking (Most Common!)
for hostname, ip_addr in routers.items():
    print(f"Device {hostname} has management IP {ip_addr}")
```

### 3.4 Modifying and Merging Dictionaries (`.pop()`, `del`, `.update()`)

* **Removing a key and capturing its value (`.pop()`):** Removes the key-value pair from the dictionary and returns the removed value so you can store or log it.
* **Deleting a key directly (`del`):** Removes the key-value pair without returning the value.
* **Merging dictionaries (`.update()`):** Combines key-value pairs from a second dictionary into the first dictionary. If both dictionaries share the same key, **the new value overwrites the existing value** ("last value wins").

```python
ca_routers = {
    "router1": "10.1.1.1",
    "router2": "10.1.1.2",
    "router3": "10.1.1.3",
}
la_routers = {
    "la_router1": "10.220.1.1",
    "la_router2": "10.220.1.2",
    "router3": "10.220.1.3",  # Overlapping key!
}

# Remove and return a key's value with .pop()
removed_ip = ca_routers.pop("router2")  # returns '10.1.1.2' and removes 'router2'

# Delete a key using del
del la_routers["la_router2"]

# Merge la_routers into ca_routers
ca_routers.update(la_routers)
# 'la_router1' is added, and 'router3' is updated to '10.220.1.3'!
```

### 3.5 Dictionary Mutability, References, and Copying

Just like lists, dictionaries are **mutable objects in memory**.

* If you write `backup_routers = routers`, you are **not** creating a copy of the dictionary. You are creating a second variable name pointing to the exact same dictionary in memory (`id(backup_routers) == id(routers)`). Modifying one will modify both!
* Use `.copy()` for a **shallow copy** (when values are simple strings or numbers).
* Use `copy.deepcopy(my_dict)` (from Python's `copy` module) when your dictionary contains **nested dictionaries or lists** so that changes to inner structures do not accidentally modify your original template.

### 3.6 Nested Data Structures: Designing Models for Network Data

When treating the network as a system, a flat dictionary is rarely enough. A single router has multiple attributes (IP, OS type, BGP AS, interfaces), and each interface has its own attributes (IP address, status, protocol, VLANs). Python lets you nest dictionaries and lists to any depth required:

1. **Dictionary of Dictionaries (`dict` of `dicts`):** Best when you want instant `O(1)` lookup by a unique identifier (such as hostname or interface name).
2. **Dictionary of Lists (`dict` of `lists`):** Best when grouping a collection of items under a category or VLAN ID (such as `{'routers': ['10.1.1.1', ...], 'switches': [...]}` or `{10: ['Gi0/1', 'Gi0/2']}`).
3. **List of Dictionaries (`list` of `dicts`):** Best when preserving a sequence of structured records returned by an API, database, or CLI parser (such as Cisco NX-API JSON tables or TextFSM output).

```python
# Dictionary of Dictionaries: Modeling a multi-vendor network inventory
my_devices = {
    "router1": {
        "device_type": "cisco_xe",
        "ip": "10.1.1.1",
        "bgp_as": 65001,
    },
    "router2": {
        "device_type": "juniper_junos",
        "ip": "10.1.1.2",
        "bgp_as": 65002,
    },
}

# Chaining keys from left to right to drill down into nested dictionaries:
# Step 1: my_devices["router1"] returns the inner dictionary for router1
# Step 2: ["device_type"] accesses the value inside that inner dictionary
print(my_devices["router1"]["device_type"])  # Output: cisco_xe
print(my_devices["router2"]["device_type"])  # Output: juniper_junos
```

> **Design Tip for Network Engineers:** Before writing code, step back and ask: *"What problem am I solving, and how will I query this data?"* If you constantly need to look up a specific interface by name (`GigabitEthernet0/0/0`), use a **dictionary of dictionaries** keyed by the interface name. If you simply need to loop through every VLAN record in order, a **list of dictionaries** works well.

### 3.7 Dictionary Comprehensions (*Optional / Intermediate Content*)

A **dictionary comprehension** dynamically builds a dictionary using curly braces `{}` and a `key: value` pair before the `for` loop:

```python
# 1. Dynamically generate a router inventory dictionary
routers = {f"router{x}": f"10.220.17.2{x}" for x in range(1, 5)}
# Output: {'router1': '10.220.17.21', 'router2': '10.220.17.22', ...}

# 2. Swap keys and values (e.g., create an IP-to-Hostname reverse lookup dictionary)
ip_to_hostname = {ip: host for host, ip in routers.items()}
# Output: {'10.220.17.21': 'router1', '10.220.17.22': 'router2', ...}
```

* **Important Rule on Duplicate Keys:** Dictionary keys must be unique. If two routers had the same IP address (`192.168.152.1` on both `router3` and `dup_router`) and you swapped keys and values, **the last value wins** (`'192.168.152.1': 'dup_router'`), overwriting `'router3'`.

## 4. Exception Handling and Stack Traces: Writing Resilient Network Code

### 4.1 Why Exceptions Happen and How `try` / `except` Works

When Python encounters an error during execution (such as accessing a list index that does not exist, a missing dictionary key, or a failed SSH connection), it raises an **exception** and immediately stops the program.

In network automation, you frequently connect to dozens or hundreds of devices in a loop. If device #5 is offline or has bad credentials, you do not want your script to crash and skip the remaining 95 devices. Instead, you use a **`try` / `except`** block to handle expected errors gracefully:

```python
my_list = []

try:
    print("Before the error")
    # This line causes an IndexError because my_list is empty!
    device = my_list[0]
    # IMPORTANT: Because an error happened above, Python immediately jumps
    # to the 'except' block. The line below is NEVER executed!
    print("After the error (never reached)")
except IndexError:
    print("Gracefully handled IndexError: The device list is empty.")

print("Outside block: Script continues executing normally!")
```

**Key Execution Rules:**
1. Python executes the lines inside the `try:` block one by one from top to bottom.
2. **If no error occurs:** All lines in `try:` finish, the `except:` block is completely skipped, and execution continues after the `try/except` structure.
3. **If an error occurs:** Python stops executing the remaining lines in `try:` at that exact moment and jumps down to check if the `except` block matches the exception type. If it matches, the handler code runs, and then the script continues normally below the block.
4. *(Practical Note on `else`)*: Some Python articles show an `else:` block attached to `try/except` (which runs only if no exception occurred). In real-world network automation, `else:` is almost never used—simply place that code inside the `try:` block or after the `try/except` block.

### 4.2 Handling Multiple Exception Types

When automating networks or parsing device data, more than one type of error might occur. You can handle multiple exceptions in two ways:

```python
my_list = ["router1"]
my_dict = {"router1": "10.1.1.1"}

# Pattern A: Single handler for multiple exception types (use a tuple)
# Useful when you want the exact same action for either failure
try:
    print(my_list[0])
    print(my_dict["router2"])
except (IndexError, KeyError):
    print("Lookup failed: Either the list index or dictionary key is missing.")

# Pattern B: Separate handlers for different exception types
# Useful when different failures require different recovery steps
try:
    print(my_list[0])          # Succeeds
    print(my_dict["router2"])  # Raises KeyError
except IndexError:
    print("List index out of range!")
except KeyError:
    print("Device key missing from inventory dictionary!")
```

### 4.3 Capturing Exception Details (`as e`) and Re-raising (`raise`)

Often you want to inspect or log the exact error message returned by Python or a library like Netmiko. Use `as e` to save the exception object into a variable.

What if you want to log the error or send a monitoring alert, **and still let the program crash** because the error is too severe to ignore? Use a bare **`raise`** statement inside your `except` block to re-raise the original exception:

```python
my_list = []

try:
    first_router = my_list[0]
except IndexError as e:
    # 1. Perform custom logging or alerting using the captured exception 'e'
    print(f"[CRITICAL ALERT] Inventory list is empty! Details: {e}")
    # 2. Re-raise the original IndexError so the script still halts execution
    raise
```

### 4.4 The Danger of Broad Exception Handling (`except Exception:`)

Python allows you to write a generic catch-all handler (`except Exception:`) that catches almost any error. While tempting, wrapping many lines of code inside a broad `except Exception:` creates **two dangerous problems** for network engineers:

1. **Corrupted Program State:** Suppose your `try` block has 15 lines of code that connect to a router, parse VLANs, and push a configuration change. If a bug or typo happens on line 3, a generic `except Exception:` catches it and lets the script keep running—even though your variables are now uninitialized or corrupt!
2. **Hiding Errors (Swallowing Exceptions):** When you hide the real error inside a broad `try/except` block, the script may crash 50 lines later with a confusing error message. You lose the original failure information and have to debug backwards to find what actually went wrong.

> **Golden Rule of Exception Handling:** Only catch **specific exception types** that you know can happen in a **narrowly scoped block of code**, and only when you know exactly how to recover from them (for example, catching an SSH timeout on a single device connection, logging `"Device unreachable"`, and continuing to the next device in the loop). If your program state is broken, **it is safer for your script to crash immediately** than to push bad configurations to your network.

### 4.5 Cleanup Operations with `finally` and Raising Custom Errors (`raise`)

* **The `finally:` Clause:** Code inside a `finally:` block **always executes**, whether an exception occurred or not. It is used for guaranteed cleanup operations—such as closing an SSH connection, releasing a configuration lock on a router, or closing a database session.
* **Raising an Exception (`raise ValueError(...)`):** You can intentionally trigger an exception in your own code when validation checks fail (fail-fast validation).

```python
ip_addr = "192.168.1.1"

# Fail-fast validation before attempting an SSH connection
if "10.220" not in ip_addr:
    raise ValueError(f"Invalid management subnet in IP: {ip_addr}. Expected 10.220.x.x")
```

```python
# Using 'finally' to guarantee session cleanup whether an error occurs or not
try:
    print("Opening database/SSH session and running commands...")
    result = my_list[0]
except IndexError:
    print("Handled error during operation.")
finally:
    print("Cleanup: Closing session safely (always executes!).")
```

### 4.6 How to Read a Python Stack Trace (Netmiko Example)

When an unhandled exception crashes your program, Python prints a **stack trace (traceback)**. Although a stack trace can look intimidating when using external libraries like Netmiko, it is simply a **top-to-bottom history of the function calls** that led to the error.

Consider the simplified Netmiko stack trace discussed in the lesson:

```text
Traceback (most recent call last):
  File "netmiko_ssh.py", line 10, in <module>
    net_connect = ConnectHandler(**device)
  File ".../netmiko/ssh_dispatcher.py", line 365, in ConnectHandler
    return ConnectionClass(*args, **kwargs)
  File ".../netmiko/base_connection.py", line 438, in __init__
    self._open()
  File ".../netmiko/tplink/tplink_jetstream.py", line 30, in session_preparation
    self._test_channel_read(pattern=r"[>#]")
  File ".../netmiko/base_connection.py", line 1500, in read_until_pattern
    raise NetmikoTimeoutException(msg)
netmiko.exceptions.NetmikoTimeoutException: Timed-out reading channel, data not available.
```

**How a Network Engineer Reads This Stack Trace:**
1. **Start at the Top (Your Code):** Look at `File "netmiko_ssh.py", line 10`. This tells you which line in **your own script** started the chain of calls (`ConnectHandler(**device)`).
2. **Follow the Call Chain Downward (Library Internals):** Your script called `ConnectHandler` in `ssh_dispatcher.py` (line 365), which called `__init__` in `base_connection.py`, which called `session_preparation` for the `tplink_jetstream` driver (line 30).
3. **Read the Bottom Lines (The Exact Root Cause):** In `tplink_jetstream.py` line 30, Netmiko tried to read the SSH channel until it saw a standard CLI prompt ending with `>` or `#` (`pattern=r"[>#]"`). Because the device never returned that expected prompt, `read_until_pattern` timed out and raised `NetmikoTimeoutException`.

## 5. Practical Network Automation Exercises (Walkthrough & Solutions)

The following five exercises from Week 4 demonstrate how to parse raw CLI text and structured output into clean Python dictionaries and sets.

### Exercise 1: Parsing `show ip interface brief` into a Dictionary (`Interface -> IP`)

**Goal:** Read `show_ip_int_brief.txt` (from a Cisco IOS-XE router), build a dictionary where keys are interface names and values are IP addresses, skip any lines without a valid IP address (such as header lines or `unassigned` interfaces), and print the dictionary using `rich.print`.

```python
from rich import print

# Sample content of show_ip_int_brief.txt:
# Interface              IP-Address      OK? Method Status                Protocol
# GigabitEthernet0/0/0   10.220.88.22    YES NVRAM  up                    up
# GigabitEthernet0/0/1   unassigned      YES NVRAM  administratively down down
# Loopback0              10.220.88.1     YES manual up                    up

ip_dict = {}

with open("show_ip_int_brief.txt") as f:
    for line in f:
        # Split the line by whitespace into fields
        fields = line.split()
        # Skip blank lines or header lines
        if not fields or fields[0] == "Interface":
            continue

        intf_name = fields[0]
        ip_addr = fields[1]

        # Skip interfaces that do not have an IP address assigned
        if ip_addr == "unassigned":
            continue

        ip_dict[intf_name] = ip_addr

print(ip_dict)
```

### Exercise 2: Building a Nested Dictionary for All Interfaces

**Goal:** Expand Exercise 1 to include **all** interfaces (both with and without an IP address). Create an outer dictionary keyed by interface name, where each value is an inner dictionary containing `"ip_addr"`, `"line_status"`, and `"line_protocol"`.

* **Parsing Nuance:** Notice that on Cisco IOS-XE, the `Status` column can be a two-word string (`administratively down`), whereas `up` or `down` is a single word. The last item (`fields[-1]`) is always `Protocol`, and everything between `Method` (`fields[3]`) and `Protocol` (`fields[-1]`) belongs to `Status`.

```python
from rich import print

interfaces = {}

with open("show_ip_int_brief.txt") as f:
    for line in f:
        fields = line.split()
        if not fields or fields[0] == "Interface":
            continue

        intf_name = fields[0]
        ip_addr = fields[1]
        # Protocol is always the last column
        line_protocol = fields[-1]
        # Status is between column index 4 and the last column
        # (handles both 'up'/'down' and 'administratively down')
        line_status = " ".join(fields[4:-1])

        interfaces[intf_name] = {
            "ip_addr": ip_addr,
            "line_status": line_status,
            "line_protocol": line_protocol,
        }

print(interfaces)
```

### Exercise 3: Looping Over a Cisco NX-OS List of Dictionaries

**Goal:** Given a list of dictionaries returned by a Cisco NX-OS switch, loop over the list and print each VLAN ID and its corresponding VLAN name.

```python
vlans = [
    {
        "vlanshowbr-vlanid": "1",
        "vlanshowbr-vlanid-utf": "1",
        "vlanshowbr-vlanname": "default",
        "vlanshowbr-vlanstate": "active",
        "vlanshowbr-shutstate": "noshutdown",
    },
    {
        "vlanshowbr-vlanid": "2",
        "vlanshowbr-vlanid-utf": "2",
        "vlanshowbr-vlanname": "VLAN0002",
        "vlanshowbr-vlanstate": "active",
        "vlanshowbr-shutstate": "noshutdown",
    },
    {
        "vlanshowbr-vlanid": "3",
        "vlanshowbr-vlanid-utf": "3",
        "vlanshowbr-vlanname": "VLAN0003",
        "vlanshowbr-vlanstate": "active",
        "vlanshowbr-shutstate": "noshutdown",
    },
    {
        "vlanshowbr-vlanid": "4",
        "vlanshowbr-vlanid-utf": "4",
        "vlanshowbr-vlanname": "VLAN0004",
        "vlanshowbr-vlanstate": "active",
        "vlanshowbr-shutstate": "noshutdown",
    },
]

for vlan_dict in vlans:
    vlan_id = vlan_dict["vlanshowbr-vlanid"]
    vlan_name = vlan_dict["vlanshowbr-vlanname"]
    print(f"VLAN ID: {vlan_id} -> VLAN Name: {vlan_name}")
```

### Exercise 4: Parsing Aruba CX `show vlan` Output and Expanding Interface Ranges

**Goal:** Parse `arubacx_show_vlan.txt` to construct a dictionary where the key is the integer VLAN ID and the value is a list of individual interfaces. When Aruba CX specifies port ranges (such as `1/1/5-1/1/9` or `lag1-lag2`), expand them into individual interface strings (`'1/1/5'`, `'1/1/6'`, `'1/1/7'`, `'1/1/8'`, `'1/1/9'`).

```python
from rich import print

vlan_map = {}

with open("arubacx_show_vlan.txt") as f:
    for line in f:
        line = line.strip()
        # Skip header lines, separator lines (---), or empty lines
        if not line or line.startswith("-") or line.startswith("VLAN"):
            continue

        fields = line.split()
        vlan_id = int(fields[0])
        # In Aruba CX 'show vlan', the interfaces column is the last column
        raw_interfaces = fields[-1].split(",")

        expanded_interfaces = []
        for intf in raw_interfaces:
            # Check if the interface entry is a range (contains '-')
            if "-" in intf:
                start_intf, end_intf = intf.split("-")
                # Case 1: Standard port range like '1/1/5-1/1/9'
                if "/" in start_intf:
                    prefix, start_port = start_intf.rsplit("/", 1)
                    _, end_port = end_intf.rsplit("/", 1)
                    for port_num in range(int(start_port), int(end_port) + 1):
                        expanded_interfaces.append(f"{prefix}/{port_num}")
                # Case 2: LAG range like 'lag1-lag2'
                elif start_intf.startswith("lag"):
                    start_num = int(start_intf.replace("lag", ""))
                    end_num = int(end_intf.replace("lag", ""))
                    for lag_num in range(start_num, end_num + 1):
                        expanded_interfaces.append(f"lag{lag_num}")
            else:
                expanded_interfaces.append(intf)

        vlan_map[vlan_id] = expanded_interfaces

print(vlan_map)
```

### Exercise 5: Converting VLAN Interface Lists to Sets and Auditing VLAN Memberships

**Goal:** Convert the interface lists from Exercise 4 into **sets**, then use set operations to answer three network engineering audit questions:
1. Which interfaces are common to **VLAN 1, VLAN 2, and VLAN 3**?
2. Which interfaces are associated with **any VLAN** on the switch?
3. Which interfaces belong to **VLAN 12 or VLAN 13** (or both)?

```python
from rich import print

# Starting from the dictionary constructed in Exercise 4:
vlan_lists = {
    1: ["1/1/3", "1/1/4"],
    2: ["1/1/1", "1/1/3", "1/1/5"],
    3: ["1/1/2", "1/1/3", "1/1/5", "1/1/6", "1/1/7", "1/1/8", "1/1/9"],
    5: ["1/1/3"],
    10: ["1/1/3", "1/1/5"],
    11: ["1/1/3"],
    12: ["1/1/3", "1/1/6", "lag1", "lag2"],
    13: ["1/1/3", "1/1/6"],
    14: ["1/1/3", "1/1/6"],
    20: ["1/1/3", "1/1/10"],
}

# Convert dictionary values from lists to sets using a dictionary comprehension
vlan_sets = {vlan_id: set(intf_list) for vlan_id, intf_list in vlan_lists.items()}

# 1. Interfaces common to VLAN 1, VLAN 2, and VLAN 3 (Intersection '&')
common_1_2_3 = vlan_sets[1] & vlan_sets[2] & vlan_sets[3]
print("1. Interfaces in VLAN 1, 2, and 3:", common_1_2_3)
# Output: {'1/1/3'} (Likely the main trunk port!)

# 2. All interfaces associated with ANY VLAN on the switch (Union '|')
all_vlan_interfaces = set()
for intf_set in vlan_sets.values():
    all_vlan_interfaces.update(intf_set)
print("2. All interfaces across any VLAN:", all_vlan_interfaces)

# 3. Interfaces associated with VLAN 12 or VLAN 13 (Union '|')
vlan_12_or_13 = vlan_sets[12] | vlan_sets[13]
print("3. Interfaces in VLAN 12 or VLAN 13:", vlan_12_or_13)
# Output: {'1/1/3', '1/1/6', 'lag1', 'lag2'}
```

## 6. Quick Reference Cheat Sheet for Network Engineers

| Task / Goal | Python Syntax | Why Use It in Network Automation? |
| :--- | :--- | :--- |
| Create a set of unique items | `vlans = {10, 20, 30}` | Automatically removes duplicate VLANs or IPs. |
| Safely remove item from a set | `vlans.discard(10)` | Removes VLAN 10 without crashing if it is already absent. |
| Find overlapping items in two sets | `site_a & site_b` | Detects duplicate IP addresses or shared trunk VLANs. |
| Find all unique items across sets | `site_a \| site_b` | Builds a master inventory of all IPs or interfaces. |
| Find items in A but not in B | `site_a - site_b` | Identifies missing VLANs or unconfigured neighbors. |
| Safe dictionary key lookup | `dev.get("ip", "N/A")` | Avoids `KeyError` when optional device fields are missing. |
| Loop over keys and values | `for k, v in dev.items():` | Cleanly iterates over device hostnames and their attributes. |
| Catch expected errors gracefully | `try: ... except KeyError as e:` | Prevents one offline router from crashing a 100-device job. |
| Guarantee session cleanup | `finally: conn.disconnect()` | Ensures SSH/NETCONF sessions close even if an error occurs. |
