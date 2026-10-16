---
title: "Week 5 — Regular Expressions"
source: "Study notes based on Kirk Byers, Learning Python for Network Engineers (Lesson 5)"
status: needs-review
---

# Week 5 Study Guide: Python Regular Expressions for Network Automation

## Treating the Network as a System: Why Regular Expressions Matter

When you manage a network manually, you connect to one router or switch at a time using SSH, run a command like `show version` or `show ip bgp summary`, and read the screen with your eyes. Your brain naturally filters out the noise and finds the software version, the serial number, or the BGP state.

When you treat the **network as a system**, your Python code must do that work across dozens or hundreds of devices automatically. To make automated decisions—such as checking if all routers run the approved OS version, verifying that every BGP neighbor is `Established`, or discovering topology connections via LLDP—your script needs **structured data** (variables, lists, and dictionaries).

Although modern network APIs (like NETCONF, RESTCONF, and gNMI) return structured JSON or XML, most production networks still rely heavily on CLI output. The CLI returns a single, unstructured block of text (a Python string). **Regular Expressions (Regex)** act as a translator between old CLI text and modern network automation:

1. **Raw Input**: Unstructured text from a router (`show version`, `show ip arp`, `show lldp neighbors`).
2. **Regex Processing**: Pattern matching that locates and extracts only the exact values you care about.
3. **Structured Output**: Clean Python strings, lists, tuples, and dictionaries ready for validation, reporting, or saving into a Source of Truth database.

> **Important Engineering Principle from [Regular Expression Introduction](https://vimeo.com/832769533)**: Regular expressions are a powerful mini-language inside Python, but it is very easy to write patterns that are too complex. In network automation, always write the **simplest and most readable pattern** that reliably extracts your data across your fleet of devices.

## 1. Regular Expression Fundamentals allow Python to Search Device Output

In [Regular Expression Introduction](https://vimeo.com/832769533), Kirk Byers explains why basic Python string methods like `.split()` or the `in` keyword are not always enough. While `.split()` works well for simple lines, CLI output often has inconsistent spacing, variable text lengths, or multi-line structures.

To use regular expressions in Python, you import the built-in `re` module and use `re.search()`:

```python
import re

# Simulated output from 'show version' on a Cisco router
data = """Cisco IOS XE Software, Version 16.08.01
Configuration register is 0x2102"""

# Basic syntax: re.search(pattern, string, flags=0)
match = re.search("Configuration register", data)

if match:
    print("Found match:", match.group(0))
```

### How `re.search()` Works

* **First Argument (`pattern`)**: The regular expression pattern you want to find. In the simplest case, it is just literal text like `"Configuration register"`.
* **Second Argument (`string`)**: The variable holding the CLI text (such as `data` or `line`).
* **Return Value (`match` object or `None`)**: If Python finds the pattern, it returns a special **Match object**. If it does not find the pattern, it returns `None`.
* **`.group(0)`**: Calling `match.group(0)` returns the entire string that matched your pattern.

## 2. Special Characters and Character Classes Build Flexible Search Patterns

Searching for exact literal text is not very useful if the value changes on every router (like IP addresses, serial numbers, or software versions). In [Special Characters](https://vimeo.com/830294637), we learn how to use special tokens to represent **types of characters** and **how many times they repeat**.

| Regex Token | Category | Meaning in Plain English | Network Automation Example |
| :--- | :--- | :--- | :--- |
| `.` | Wildcard | Matches any single character (except a newline `\n` by default). | `10.1.1.` matches `10` + any char + `1` (warning: `.` is not a literal dot unless escaped!). |
| `*` | Quantifier (Greedy) | Matches the previous item **0 or more times** (matches as much as possible). | `.*` grabs an entire line of CLI output, including an empty string. |
| `+` | Quantifier (Greedy) | Matches the previous item **1 or more times** (requires at least one match). | `\d+` matches a 1-digit, 2-digit, or 3-digit octet in an IP address. |
| `?` | Quantifier / Modifier | Alone: matches **0 or 1 time**. After `*` or `+`: makes them **non-greedy** (`*?`, `+?`). | `.*?` matches as few characters as possible until the next part of the pattern. |
| `\s` | Character Class | Matches any **whitespace** character (space, tab `\t`, newline `\n`, carriage return `\r`). | `\s+` handles CLI columns separated by 1 space or 10 spaces. |
| `\S` | Character Class | Matches any **non-whitespace** character (everything except spaces/tabs/newlines). | `\S+` grabs a full interface name like `GigabitEthernet0/0/1` or a hex value `0x2102`. |
| `\w` | Character Class | Matches any **word** character: letters (`a-z`, `A-Z`), numbers (`0-9`), and underscore (`_`). | `\w+` matches hostnames or hexadecimal MAC address segments. |
| `\d` | Character Class | Matches any **digit** from `0` to `9`. | `\d+\.\d+\.\d+\.\d+` matches an IPv4 address. |
| `[...]` | Custom Class | Matches any single character listed inside the square brackets. | `[\d\.]+` matches a version string made of digits and dots like `16.8.1`. |
| `(...)` | Capture Group / OR | Saves the matched substring for extraction, or groups logical OR options `(up\|down)`. | `Processor board ID (\S+)` saves only the serial number. |
| `^` and `$` | Anchors | Matches the **beginning** (`^`) and **end** (`$`) of the string (or line with `re.MULTILINE`). | `^Interface` ensures the word "Interface" is at the start of the line. |
| `\` | Escape Character | Turns a special character into a literal character. | `\.` matches an actual period in an IP address instead of "any character". |

## 3. Greedy vs. Non-Greedy Matching Controls How Much Text Python Grabs

In [(Somewhat) Simple Examples](https://vimeo.com/830644262), we see how quantifiers behave on a real line from Cisco `show version`:

```python
import re

line = "Cisco IOS XE Software, Version 16.08.01, RELEASE SOFTWARE (fc3)"
alt_line = "Cisco   Fuji"
```

### Understanding Greedy vs. Non-Greedy Behavior

By default, `*` and `+` are **greedy**. They try to consume the maximum number of characters possible while still allowing the overall pattern to succeed. Adding `?` immediately after `*` or `+` makes them **non-greedy** (lazy), meaning they match the minimum number of characters required:

* `re.search(".", line)` matches only `"C"` (the first single character).
* `re.search("..", line)` matches `"Ci"` (the first two characters).
* `re.search(".*", line)` matches the **entire line** because `*` is greedy and repeats `.` as many times as possible.
* `re.search(".*?", line)` matches `""` (the empty/null string!) because `*` allows zero matches, and `?` asks for the fewest characters possible.
* `re.search(".+?", line)` matches `"C"` because `+` requires at least one character, and `?` stops after just one.

### Matching Variable CLI Whitespace

In CLI tables, columns often have different numbers of spaces depending on the length of the values. Instead of counting spaces manually, use `\s+` (one or more whitespace characters):

```python
# Matches 'Cisco', followed by 1 or more spaces, followed by 'Fuji'
m1 = re.search(r"Cisco\s+Fuji", alt_line)

# Matches 1 or more non-whitespace characters ('Cisco'), spaces, and 'Fuji'
m2 = re.search(r"\S+\s+Fuji", alt_line)

# Matches 1 or more word characters ('Cisco'), spaces, and 'Fuji'
m3 = re.search(r"\w+\s+Fuji", alt_line)
```

## 4. Watching Out for Greedy `.*` Traps When Extracting OS Versions

In [Additional Examples](https://vimeo.com/830428490), Kirk demonstrates a very common mistake network engineers make when combining `.*` with digits or custom character classes.

Suppose we have this line from a router:

```python
line = "Cisco IOS XE Software, Version 16.08.01, RELEASE SOFTWARE (fc3)"
```

### Trap 1: `^Cisco.*\d+`

If you write `re.search(r"^Cisco.*\d+", line)`, you might think `.*` stops at `Version ` and `\d+` matches `16`. **It does not!**

Because `.*` is greedy, Python pushes `.*` as far to the right as possible while still finding at least one digit (`\d+`). Since there is a `3` inside `(fc3)` at the end of the line, `.*` consumes everything up to `(fc` and `\d+` matches `3`!

### Trap 2: `^Cisco.*([\d\.]+), REL`

Even if you create a custom character class `[\d\.]+` (digits and literal periods) and anchor the right side with `, REL`, writing `re.search(r"^Cisco.*([\d\.]+), REL", line)` still fails to get `16.08.01`!

Why? Because `.*` is greedy! It swallows `Version 16.08.0` and leaves only the final `1` for `([\d\.]+)`. So `m.group(1)` returns `"1"` instead of `"16.08.01"`.

### The Fix: Anchor Before the Capture Group

To stop `.*` from eating your version number, place literal text (or a space) immediately **before** the capture group so `.*` must stop before the version starts:

```python
import re

line = "Cisco IOS XE Software, Version 16.08.01, RELEASE SOFTWARE (fc3)"

# By putting 'Version ' (or 'ion ') before the capture group,
# '.*' must stop before '16.08.01'
m = re.search(r"^Cisco.*Version ([\d\.]+), REL", line)
if m:
    print("Extracted OS Version:", m.group(1))  # Output: 16.08.01
```

## 5. Capture Groups and Raw Strings (`r"..."`) Keep Data Extraction Clean

In [Capture Groups and Raw Strings](https://vimeo.com/830646534), we learn two essential habits for writing production-ready network automation code.

### Why You Should Always Use Raw Strings (`r"..."`)

Both Python strings and Regular Expressions use the backslash (`\`) as a special character. For example, in normal Python strings, `\n` means a newline and `\t` means a tab.

When writing regex patterns, we want `\s`, `\d`, and `\w` to be interpreted by the **Regular Expression engine**, not by Python's string parser. Placing an `r` in front of the string quotes (`r"..."`) creates a **Raw String**, which turns off Python's special backslash processing and passes backslashes directly to `re`:

```python
import re

data = "Configuration register is 0x2102"

# Always prefix regex patterns with r"..."
m = re.search(r"Configuration register is (.*)", data)
if m:
    print("Full match:", m.group(0))        # Configuration register is 0x2102
    print("Captured value:", m.group(1))    # 0x2102
```

### Stopping Capture Groups at Delimiters

What if a line has multiple commas and you want to capture only the version number before the first comma?

```python
import re

line = "Cisco IOS Software, Version 15.4(2)T1, RELEASE SOFTWARE (fc1), Extra Info"

# Greedy (.*) with a comma after it would match up to the LAST comma!
# Non-greedy (.*?) stops at the FIRST comma after 'Version ':
m = re.search(r"Version (.*?),", line)
if m:
    print("OS Version:", m.group(1))  # Output: 15.4(2)T1
```

## 6. Anchors (`^` and `$`) Need `re.MULTILINE` for Multi-Line CLI Output

In [Anchors and re.MULTILINE](https://vimeo.com/830685707), we learn a critical detail about how Python handles multi-line CLI outputs like a full `show version` or `show running-config`.

By default in Python:
* `^` matches only the **very beginning of the entire string**.
* `$` matches only the **very end of the entire string**.

If you read a 50-line `show version` file into a single string variable `data` and search for `r"^Configuration register is (\S+)$"`, **it will return `None`** because that line is in the middle or bottom of the string, not at the very beginning!

### Enabling Line-by-Line Anchor Behavior with `re.MULTILINE` (`re.M`)

To make `^` and `$` match the beginning and end of **each individual line** inside a multi-line string, pass `flags=re.MULTILINE` (or its shorthand `flags=re.M`):

```python
import re

show_ver = """Cisco IOS XE Software, Version 16.08.01
Router uptime is 3 weeks, 2 days
Configuration register is 0x2102
"""

# Without re.M, ^ and $ only check the start and end of the whole string -> returns None
failed_match = re.search(r"^Configuration register is (\S+)$", show_ver)

# With flags=re.M (or re.MULTILINE), ^ and $ check every line -> succeeds!
m = re.search(r"^Configuration register is (\S+)$", show_ver, flags=re.M)
if m:
    print("Config Register:", m.group(1))  # Output: 0x2102
```

## 7. `re.findall()` Converts Repeating CLI Tables into Lists and Dictionaries

In [re.findall()](https://vimeo.com/830690686), we move from extracting a single value (`re.search()`) to parsing entire tables of repeating data—such as ARP tables (`show ip arp`), MAC address tables (`show mac address-table`), or routing tables (`show ip route`).

While `re.search()` stops after the first match, `re.findall(pattern, data)` scans the entire string and returns all matches:

* **With 1 capture group**: `re.findall()` returns a **list of strings** (`['10.220.88.1', '10.220.88.20', ...]`).
* **With 2 or more capture groups**: `re.findall()` returns a **list of tuples**, binding the captured values from each row together (`[('10.220.88.1', '0062.ec29.70fe'), ...]`).

### Keeping Complex Patterns Readable with Python f-strings

Long regex patterns for multi-column tables can quickly become hard to read. Kirk shows a great engineering practice: define smaller building-block patterns first, then combine them using an **f-string** (`rf"..."`):

```python
import re

arp_output = """Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.220.88.1             5   0062.ec29.70fe  ARPA   GigabitEthernet0/0/0
Internet  10.220.88.20            -   c89c.1dea.0eb6  ARPA   GigabitEthernet0/0/0
Internet  10.220.88.22           12   a093.5141.b780  ARPA   GigabitEthernet0/0/0
"""

# Define readable sub-patterns for IP and MAC addresses
ip_addr = r"\d+\.\d+\.\d+\.\d+"
mac_addr = r"\w+\.\w+\.\w+"

# Combine them using a raw f-string (rf"...")
# Notice [-\d]+ matches either a hyphen '-' (local interface) or digits (age in minutes)
pattern = rf"^Internet\s+({ip_addr})\s+[-\d]+\s+({mac_addr})\s+"

# Extract all rows as a list of (ip, mac) tuples
arp_entries = re.findall(pattern, arp_output, flags=re.M)
print("List of tuples:", arp_entries)

# Convert directly into a Python dictionary for fast IP -> MAC lookups!
arp_dict = dict(arp_entries)
print("ARP Dictionary:", arp_dict)
```

## 8. Match Logic Prevents Automation Scripts from Crashing

In [Match logic](https://vimeo.com/832457474), we look at defensive coding for network automation. When your script connects to 100 devices, one device might run a different software version or have an unconfigured feature.

If `re.search()` fails to find a match, it returns `None`. If you immediately call `match.group(1)` without checking, Python raises an `AttributeError: 'NoneType' object has no attribute 'group'` and your automation script crashes!

Always wrap your extraction in an `if match:` conditional block:

```python
import re

output = "Interface GigabitEthernet0/0 is down, line protocol is down"

match = re.search(r"IP address is (\S+)", output)

# In Python, a Match object evaluates to True, while None evaluates to False
if match:
    print("IP Address:", match.group(1))
else:
    print("No IP address configured on this interface.")
```

## 9. `re.DOTALL` Allows the Dot (`.`) to Match Across Multiple Lines

In [re.DOTALL](https://vimeo.com/832460190), we review a major rule of the dot (`.`) special character: **by default, `.` matches any character EXCEPT a newline (`\n`)**.

When you use `.*`, it stops at the end of the current line. However, in networking, a single logical record often spans multiple lines—for example, a neighbor block in `show lldp neighbors detail` or `show cdp neighbors detail`, where a record starts with `Chassis id:` on line 1 and ends with `Vlan ID:` 15 lines later.

To allow `.` to match every character **including newlines**, pass `flags=re.DOTALL` (or its Python shorthand `flags=re.S`):

> **Practical Note on Python Shorthand**: In the video lecture, the slide mentions `re.D` as an abbreviation for `re.DOTALL`, but in Python's standard `re` library, the single-letter shorthand for `re.DOTALL` (Single-line mode) is actually **`re.S`**. Writing `re.DOTALL` in full is always the clearest and safest choice in your scripts!

```python
import re

multi_line_text = """Line 1: RouterA
Line 2: SwitchB"""

# Fails (returns None) because '.' cannot cross the '\n' between Line 1 and Line 2
m_fail = re.search(r"^Line 1.*SwitchB$", multi_line_text)

# Succeeds because flags=re.DOTALL allows '.' to match '\n'
m_success = re.search(r"^Line 1.*SwitchB$", multi_line_text, flags=re.DOTALL)
if m_success:
    print("Matched across multiple lines:\n", m_success.group(0))
```

## 10. `re.escape()` Protects Automation Scripts When Matching Dynamic Device Prompts

In [re.escape()](https://vimeo.com/832488661), Kirk connects regular expressions directly to how SSH automation libraries (like Netmiko) work under the hood.

When an automation tool logs into a router or Linux server via SSH and sends a command, how does it know when the device has finished printing the output? It watches the incoming text stream until it sees the **device prompt** again!

However, device prompts come from external devices or user input and often contain characters that have **special meaning in regex**, such as square brackets `[` `]`, parentheses `(` `)`, or a dollar sign `$`:

```text
[user@router-01 ~]$
```

If you pass `[user@router-01 ~]$` directly into `re.search()`, the regex engine treats `[...]` as a custom character class and `$` as an end-of-string anchor, breaking your prompt detection!

### Converting Any Dynamic String into a Literal Pattern with `re.escape()`

Calling `re.escape(dynamic_string)` automatically places a backslash (`\`) in front of every special regex character so Python treats the entire string as **exact literal text**:

```python
import re

device_prompt = "[user@router-01 ~]$ "
cli_session_output = """show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     10.1.1.1        YES NVRAM  up                    up
[user@router-01 ~]$ """

# Escape all special regex characters in the dynamic prompt
safe_prompt_pattern = re.escape(device_prompt)
print("Escaped pattern:", safe_prompt_pattern)
# Output: \[user@router\-01\ \~\]\$\ 

if re.search(safe_prompt_pattern, cli_session_output):
    print("Detected end of command output safely!")
```

## 11. Named Capture Groups (`(?P<name>...)`) Turn CLI Output Directly into Dictionaries

In [Named Capture Groups](https://vimeo.com/832490540), we learn an intermediate feature that makes network automation scripts much easier to maintain.

When you extract 5 or 6 fields from a complex output (like BGP neighbor details), keeping track of `m.group(1)`, `m.group(2)`, ..., `m.group(5)` is confusing and fragile. If someone adds a new set of parentheses in the middle of the pattern, all the group numbers shift!

Using Python's **Named Capture Group** syntax `(?P<group_name>pattern)`, you assign a descriptive key name to each captured value:

* Retrieve a specific field by name: `m.group("group_name")`
* Retrieve **all** named fields at once as a Python dictionary: `m.groupdict()`

```python
import re

data = "Configuration register is 0x2102"

# Syntax: (?P<name>pattern)
m = re.search(r"^Configuration register is (?P<confreg>\S+)$", data)

if m:
    # Access by name instead of number
    print("Using .group('confreg'):", m.group("confreg"))
    
    # Or get a clean dictionary ready for JSON serialization or APIs!
    print("Using .groupdict():", m.groupdict())
    # Output: {'confreg': '0x2102'}
```

## 12. Visual Debugging with Regex101 Accelerates Pattern Design

In [regex101.com](https://vimeo.com/832496547), Kirk demonstrates how to build and troubleshoot regular expressions interactively before pasting them into your Python scripts:

1. **Select the Python Flavor**: In the left navigation menu of Regex101, always select **Python** so the engine supports Python-specific syntax like `(?P<name>...)`.
2. **Paste Real CLI Output**: Copy a snippet of `show version`, `show ip bgp neighbors`, or `show lldp neighbors` into the **Test String** box.
3. **Configure Regex Flags**: Click the flag icon on the right side of the Regular Expression input bar to toggle **multiline (`m`)** (`re.MULTILINE`) or **single line (`s`)** (`re.DOTALL`, where dot matches newline).
4. **Inspect Match & Group Colors**: As you type your pattern, the tool highlights the full match (`group(0)`) in one color and each capture group (`group(1)`, `group(2)`) in distinct colors, while the right-hand **Explanation** and **Match Information** panels explain every token step by step and a **Quick Reference** box at the bottom right lets you look up tokens instantly.

## Practical Network Automation Lab: Step-by-Step Solutions to Week 5 Exercises

Below is a complete guide to solving the 5 hands-on exercises from [Week 5 Exercises on GitHub](https://github.com/twin-bridges/learning_python/tree/main/lesson5/exercises), explaining both the regex mechanics and how each exercise fits into treating the network as a system.

### Exercise 1: Extracting Hardware Inventory from Cisco IOS-XE (`show_version.txt`)

**System Goal**: Automatically collect hardware models and serial numbers from devices to keep an asset management database (like NetBox) accurate.

**Target CLI Lines**:
```text
cisco C1111-4P (1RU) processor with 1401823K/6147K bytes of memory.
Processor board ID FGL222290LB
```

**Python Solution**:
```python
import re

show_version = """cisco C1111-4P (1RU) processor with 1401823K/6147K bytes of memory.
Processor board ID FGL222290LB"""

# Match 'cisco ', capture the non-whitespace model number, followed by ' (1RU) processor' or ' processor'
model_match = re.search(r"^cisco (?P<model>\S+).*processor with", show_version, flags=re.M)

# Match 'Processor board ID ' and capture the serial number
serial_match = re.search(r"^Processor board ID (?P<serial>\S+)$", show_version, flags=re.M)

if model_match and serial_match:
    model = model_match.group("model")
    serial_number = serial_match.group("serial")
    print(f"Device Model:  {model}")
    print(f"Serial Number: {serial_number}")
```

**Why It Works**:
* `flags=re.M` allows `^` and `$` to match individual lines inside the full `show_version.txt` file.
* `\S+` grabs the continuous string of non-whitespace characters (`C1111-4P` and `FGL222290LB`).

### Exercise 2: Auditing BGP Control Plane State (`show_ip_bgp_neighbors.txt`)

**System Goal**: Parse BGP neighbor state into structured fields so an automated health check can verify that peering sessions are `Established` with the expected Autonomous System (AS).

**Target CLI Lines**:
```text
BGP neighbor is 10.220.88.38,  remote AS 44, external link
  BGP version 4, remote router ID 10.220.88.38
  BGP state = Established, up for 11w0d
```

**Python Solution (Using Named Capture Groups)**:
```python
import re

bgp_output = """BGP neighbor is 10.220.88.38,  remote AS 44, external link
  BGP version 4, remote router ID 10.220.88.38
  BGP state = Established, up for 11w0d"""

# We can extract across lines or search each line with named capture groups
pattern = (
    r"^BGP neighbor is (?P<bgp_neighbor_ip>[\d\.]+),\s+remote AS (?P<remote_as>\d+).*?\n"
    r"\s+BGP version (?P<bgp_version>\d+), remote router ID (?P<remote_router_id>[\d\.]+)\n"
    r"\s+BGP state = (?P<bgp_state>\w+),"
)

m = re.search(pattern, bgp_output, flags=re.M)
if m:
    bgp_info = m.groupdict()
    for field, value in bgp_info.items():
        print(f"{field}: {value}")
```

**Why It Works**:
* Named capture groups (`?P<bgp_neighbor_ip>`, `?P<remote_as>`, etc.) immediately give us a clean dictionary via `m.groupdict()`, making it easy to print or export to JSON.
* You can also split this into three smaller `re.search()` calls (one for each line) if you prefer shorter patterns!

### Exercise 3: Building an IP-to-MAC Lookup Dictionary from Arista EOS (`arista_show_ip_arp.txt`)

**System Goal**: Convert a switch's ARP table into a Python dictionary (`{ip_address: mac_address}`) to trace endpoint locations across the network.

**Python Solution**:
```python
import re

arista_arp = """Address         Age (sec)  Hardware Addr   Interface
10.220.88.1             0  0062.ec29.70fe  Vlan1, Ethernet1
10.220.88.20            0  c89c.1dea.0eb6  Vlan1, Ethernet2
10.220.88.28            0  5254.abbe.5b7b  Vlan1, Management1
"""

# Capture Group 1: IP address (\d+\.\d+\.\d+\.\d+)
# Capture Group 2: MAC address (\w+\.\w+\.\w+)
pattern = r"^(\d+\.\d+\.\d+\.\d+)\s+\d+\s+(\w+\.\w+\.\w+)\s+"

# re.findall() with 2 capture groups returns a list of 2-element tuples: [(ip, mac), ...]
arp_tuples = re.findall(pattern, arista_arp, flags=re.M)

# Directly cast the list of (key, value) tuples into a dictionary
arp_dict = dict(arp_tuples)
print("Arista ARP Dictionary:")
print(arp_dict)
```

**Why It Works**:
* `re.findall()` automatically loops over the entire ARP output and collects every matching row as a `(ip, mac)` tuple.
* Passing a list of 2-value tuples into `dict()` turns the first element (IP) into the dictionary key and the second element (MAC) into the dictionary value in one line of code.

### Exercise 4: Discovering Physical Topology from NX-OS LLDP Detail (`show_lldp.txt`)

**System Goal**: Break a multi-block CLI output into individual neighbor sections, then extract the local interface, remote device name, and remote interface for each neighbor to verify cabling and topology.

**Target Structure**: Four LLDP entries, each starting with `Chassis id:` and ending with `Vlan ID: ...`.

**Python Solution**:
```python
import re

lldp_output = """Chassis id: 0026.9815.c160
Port id: Ethernet1/1
Local Port id: Eth1/1
Port Description: Uplink to Core1
System Name: nxos-core1.domain.com
System Description: Cisco Nexus Operating System (NX-OS) Software
Vlan ID: 100

Chassis id: 0026.9815.c220
Port id: Ethernet1/2
Local Port id: Eth1/2
Port Description: Uplink to Core2
System Name: nxos-core2.domain.com
System Description: Cisco Nexus Operating System (NX-OS) Software
Vlan ID: 100
"""

# Step 1: Extract each LLDP block from 'Chassis id:' through its own 'Vlan ID:' line.
# - Non-greedy '.*?' (with re.DOTALL) stops at the FIRST '^Vlan ID:' it finds.
# - '[^\n]*' (not '.*') takes the rest of that single line. With re.DOTALL a greedy
#   '.*$' would run to the end of the whole output and merge every neighbor into ONE block!
lldp_blocks = re.findall(r"^Chassis id:.*?^Vlan ID:[^\n]*$", lldp_output, flags=re.DOTALL | re.M)

print(f"Found {len(lldp_blocks)} LLDP neighbor sections:\n")

# Step 2: Loop through each neighbor section and extract the 3 topology fields
for block in lldp_blocks:
    local_port_m = re.search(r"^Local Port id:\s+(\S+)", block, flags=re.M)
    remote_sys_m = re.search(r"^System Name:\s+(\S+)", block, flags=re.M)
    remote_port_m = re.search(r"^Port id:\s+(\S+)", block, flags=re.M)

    if local_port_m and remote_sys_m and remote_port_m:
        local_port = local_port_m.group(1)
        remote_system_name = remote_sys_m.group(1)
        remote_port = remote_port_m.group(1)
        print(f"Local Port: {local_port}  -->  Remote Neighbor: {remote_system_name} ({remote_port})")
```

**Why It Works**:
* **Why `.*?` is essential in Step 1**: When `re.DOTALL` is active, a greedy `.*` would start at the first `Chassis id:` and eat all the way down to the fourth (last) `Vlan ID:`, giving you 1 giant block instead of 4 separate blocks! Using non-greedy `.*?` stops each match at the very first `Vlan ID:` line it encounters.
* **Why the tail is `[^\n]*$` and not `.*$`**: the same trap appears a second time at the end of the pattern. With `re.DOTALL`, a greedy `.*` after `Vlan ID:` also crosses newlines, runs to the end of the whole output and lets `$` match there, so `findall()` returns **one** merged block and the loop prints only the first neighbor. `[^\n]*` cannot cross a line break, so each block ends on its own `Vlan ID:` line.
* **Divide and Conquer**: Splitting a large output into per-entity blocks first (`re.findall` with `re.DOTALL`) and then running simple single-line searches (`re.search`) inside each block is one of the cleanest design patterns in network automation.

### Exercise 5: Validating IPv6 Interface State on Aruba CX (`aruba_cx_show_ipv6_intf.txt`)

**System Goal**: Verify interface operational state, administrative state, and IPv6 address assignment across multi-vendor switches.

**Target CLI Lines**:
```text
Interface 1/1/1 is up
Admin state is up
IPv6 address:
   2001:0db8:85a3:0000:0000:8a2e:0370:7334/24 [VALID]
```

**Python Solution**:
```python
import re

aruba_ipv6 = """Interface 1/1/1 is up
Admin state is up
IPv6 address:
   2001:0db8:85a3:0000:0000:8a2e:0370:7334/24 [VALID]"""

# Extract all 4 values using named capture groups across lines
pattern = (
    r"^Interface (?P<intf_name>\S+) is (?P<intf_state>\S+)\n"
    r"Admin state is (?P<admin_state>\S+)\n"
    r"IPv6 address:\n"
    r"\s+(?P<ipv6_addr>\S+)\s+\[VALID\]"
)

m = re.search(pattern, aruba_ipv6, flags=re.M)
if m:
    print(f"Interface Name:  {m.group('intf_name')}")
    print(f"Interface State: {m.group('intf_state')}")
    print(f"Admin State:     {m.group('admin_state')}")
    print(f"IPv6 Address:    {m.group('ipv6_addr')}")
```

## Quick Reference Summary for Network Engineers

| Task in Network Automation | Best Regex Tool / Flag | Pattern Strategy |
| :--- | :--- | :--- |
| Extract 1 value from a line (e.g., Serial Number, OS Version) | `re.search(r"...", data, flags=re.M)` | Put literal CLI labels outside `(...)` and the target value inside `(\S+)` or `([\d\.]+)`. |
| Extract all rows from a table (e.g., ARP, MAC, BGP summary) | `re.findall(r"...", data, flags=re.M)` | Put parentheses around each column you want; returns a list of strings (1 group) or tuples (2+ groups). |
| Split multi-line neighbor/interface records into separate blocks | `re.findall(r"^Start.*?^End.*$", data, flags=re.DOTALL \| re.M)` | Always combine `re.DOTALL` with **non-greedy** `.*?` so blocks do not merge together. |
| Build a dictionary directly from a single match | `(?P<field_name>...)` + `m.groupdict()` | Use named capture groups when parsing 3+ fields from a command like `show ip bgp neighbors`. |
| Build a lookup dictionary from a two-column CLI table | `dict(re.findall(r"... (key) ... (val) ...", data))` | Capture the key in Group 1 and value in Group 2, then pass the list of tuples into `dict()`. |
| Match a dynamic router prompt safely (`router(config-if)#`) | `re.escape(prompt_str)` | Escapes `()`, `[]`, `$`, and `.` automatically so they are matched as literal characters. |
