# Learning Python for Network Engineers — Week 2 Study Guide
**Course Reference:** Kirk Byers (*Learning Python for Network Engineers* / Lesson 2)  
**Target Audience:** Network Engineers transitioning to Network Automation  
**Language Level:** English (B1/B2 Intermediate)

---

## 1. Introduction: Scaling Data and State in Network Automation

In Week 1, you learned how to set up isolated virtual environments (`venv`), follow PEP 8 standards, and store simple text values in variables. However, when you treat the **network as a system**, a single string variable is not enough. 

To automate real-world infrastructure, your scripts need to:
- Calculate subnet sizes, interface counters, and link utilization (**Numbers: Integers & Floats**).
- Make logical decisions based on whether a BGP peer is up or a configuration value is missing (**Booleans & `None`**).
- Read CLI outputs (`show version`), save backup configurations, and record audit logs safely (**Files & Context Managers**).
- Group dozens of routers, VLANs, and routing tables into organized collections (**Lists & Tuples**).
- Understand how Python manages computer memory so you do not accidentally overwrite production device data (**Mutable vs. Immutable Objects & Shallow vs. Deep Copy**).

*(Note: While `sets` are mentioned in the course introduction, Kirk Byers defers `sets` to a later lesson in the course so we can focus deeply on lists and tuples first.)*

---

## 2. Numbers in Python: Integers (`int`) and Floats (`float`)

Network engineering is full of numbers. Python divides numbers into two main data types:

1. **Integers (`int`):** Whole numbers without decimals (for example: VLAN IDs like `100`, BGP AS numbers like `65001`, TCP port numbers like `22`, or packet counters).
2. **Floats (`float`):** Numbers with a decimal point (for example: interface utilization like `78.5%`, optical transceiver power levels like `-3.42` dBm, or round-trip latency like `12.35` ms).

```python
# Integer assignment
ssh_port = 22
print(type(ssh_port))       # Output: <class 'int'>

# Float assignment
optical_rx_dbm = -2.45
print(type(optical_rx_dbm)) # Output: <class 'float'>
```

### Standard Math Operators (`+`, `-`, `*`, `/`)
You can perform standard arithmetic with both integers and floats. 

> **CRITICAL RULE FOR DIVISION (`/`):**  
> In Python 3, standard division using a single slash (`/`) **always returns a `float`**, even if the two numbers divide evenly!

```python
vlan_base = 100
print(vlan_base + 10)  # Addition: 110 (int)
print(vlan_base - 20)  # Subtraction: 80 (int)
print(vlan_base * 2)   # Multiplication: 200 (int)

# Division always produces a float!
links = 4
cores = 2
links_per_core = links / cores
print(links_per_core)       # Output: 2.0
print(type(links_per_core)) # Output: <class 'float'>
```

### Special Math Operators: Modulo (`%`) and Power (`**`)

#### 1. The Modulo Operator (`%`)
The **modulo operator (`%`)** divides two numbers and returns only the **remainder** of that division.
- If `9 % 2` is evaluated: $2$ goes into $9$ four times ($2 \times 4 = 8$) with a remainder of $1$. So `9 % 2` returns `1`.
- If `9 % 3` is evaluated: $3$ goes into $9$ evenly ($3 \times 3 = 9$) with a remainder of $0$. So `9 % 3` returns `0`.

**Networking Use Case:** How do you automatically split 100 VLANs across two Core Switches (even VLANs on `Core-01`, odd VLANs on `Core-02`)? You check `vlan_id % 2`:
- If `vlan_id % 2 == 0`, the VLAN is **even**.
- If `vlan_id % 2 == 1`, the VLAN is **odd**.

```python
vlan_id = 105
remainder = vlan_id % 2
print(remainder)  # Output: 1 (Odd VLAN -> assign to Core-02 as primary root)
```

#### 2. Raising to a Power (`**`)
The double-asterisk operator (`**`) raises a number to an exponent (for example, `2 ** 3` calculates $2^3 = 8$).

**Networking Use Case:** Subnetting math! Every network engineer calculates host capacity using powers of $2$ ($2^{\text{host bits}}$):
```python
# Calculate total IPv4 addresses in a /24 subnet (8 host bits)
host_bits = 8
total_ips = 2 ** host_bits
usable_hosts = (2 ** host_bits) - 2

print("Total IPs in /24:", total_ips)       # Output: 256
print("Usable hosts in /24:", usable_hosts) # Output: 254
```

### Rounding Floats with `round()`
When calculating link bandwidth percentages or SLA latency averages, Python floats often produce long repeating decimals in memory. You can use the built-in `round(number, ndigits)` function to round a float to a specific number of decimal places.

```python
# Example: 4 divided by 3 produces a repeating decimal
raw_latency = 4 / 3
print(raw_latency)  # Output: 1.3333333333333333

# Round to 2 decimal places for a clean network report
clean_latency = round(raw_latency, 2)
print(clean_latency)  # Output: 1.33
```

### Increment (`+=`) and Decrement (`-=`) Counters
When your script loops through network devices, you often want a counter variable to keep track of how many interfaces are `UP` or how many login attempts remain.

Instead of writing `i = i + 1`, Python provides a clean shorthand called `+=` (increment) and `-=` (decrement):

```python
# Initialize counter at zero
active_ports = 0

# Standard way to add 1
active_ports = active_ports + 1  # active_ports is now 1

# Pythonic shorthand (exact same behavior)
active_ports += 1                # active_ports is now 2
active_ports += 1                # active_ports is now 3
print("Active ports:", active_ports)

# Decrementing a retry counter using -=
ssh_retries_left = 3
ssh_retries_left -= 1            # ssh_retries_left is now 2
print("Retries remaining:", ssh_retries_left)
```

---

## 3. Booleans (`bool`) and the `None` Type

### Boolean Values (`True` and `False`)
In Python, a Boolean (`bool`) represents a binary truth value: **`True`** or **`False`**.
- **Syntax Rule:** You must capitalize the first letter (`True`, `False`) and **never** put quotes around them (`"True"` with quotes is a string, not a boolean!).

```python
interface_up = True
bgp_down = False

print(type(interface_up))  # Output: <class 'bool'>
```

### Boolean Logic: `and`, `or`, `not`
When building conditional checks (like `if` statements) to validate network state, you combine booleans using three logical operators:

| Operator | Rule | Network Automation Example |
| :--- | :--- | :--- |
| **`and`** | Returns `True` **only if both** sides are `True`. | `link_up and ospf_full` (Both physical link and OSPF adjacency must be healthy). |
| **`or`** | Returns `True` if **at least one** side is `True`. | `is_cisco or is_arista` (Run command if device matches either vendor). |
| **`not`** | Inverts the boolean value (`True` becomes `False`, `False` becomes `True`). | `not in_maintenance` (Only push configs if the device is NOT in maintenance mode). |

```python
link_up = True
bgp_established = False

# 'and' requires BOTH to be True
print(link_up and bgp_established)  # Output: False

# 'or' requires AT LEAST ONE to be True
print(link_up or bgp_established)   # Output: True

# 'not' flips the value (Logical Complement)
print(not bgp_established)          # Output: True
```

### "Truish" Values: Evaluating Non-Booleans in a Boolean Context
In Python, you do not have to pass a strict `True` or `False` into an `if` statement. You can evaluate strings, integers, floats, or lists directly in a **Boolean context** (sometimes called *"truish"* or *truthy/falsy* behavior).

How does Python decide if a string or a list is `True` or `False`?
> **The Golden Rule:** For every data type, Python defines **one single "empty" or "zero" value as `False`**. Every other value of that type evaluates to **`True`**!

| Data Type | The ONE Value That Evaluates to `False` | Values That Evaluate to `True` |
| :--- | :--- | :--- |
| **String (`str`)** | `""` (The null / empty string) | Any string with characters (`"Gi0/1"`, `"0"`, `"False"`) |
| **Integer (`int`)** | `0` (Zero) | Any non-zero integer (`1`, `100`, `-5`) |
| **Float (`float`)** | `0.0` (Zero float) | Any non-zero float (`3.3`, `-0.01`) |
| **List (`list`)** | `[]` (The empty list) | Any list with at least 1 item (`["10.0.0.1"]`) |
| **Dictionary (`dict`)** | `{}` (The empty dictionary) | Any dictionary with key-value pairs |
| **Set (`set`)** | `set()` (The empty set) | Any non-empty set |

You can test how Python evaluates any variable in a boolean context using the built-in `bool()` function:

```python
# Testing Strings in a Boolean Context
port_description = ""              # Empty string (no description on interface)
print(bool(port_description))      # Output: False

port_description = "Uplink_to_Core"
print(bool(port_description))      # Output: True

# Testing Integers and Lists in a Boolean Context
crc_errors = 0
print(bool(crc_errors))            # Output: False (0 errors)

bgp_neighbors = ["10.1.1.1", "10.1.1.2"]
print(bool(bgp_neighbors))         # Output: True (list is not empty)
```

**Why this is great for Network Engineers:**  
Instead of writing `if len(bgp_neighbors) > 0:`, you can simply write `if bgp_neighbors:` to check if your list of BGP neighbors contains data!

### The Special `None` Type (`NoneType`)
Python has a special data type called **`None`** (written with a capital `N` and no quotes). It represents the **absence of a value** (similar to `null` in other languages or JSON).

1. **Its Own Type:** `type(None)` returns `<class 'NoneType'>`. A `NoneType` variable can only ever hold one possible value: `None`.
2. **Boolean Context:** `None` always evaluates to **`False`** (`bool(None)` is `False`).
3. **Default Return Value of Functions:** If a Python function finishes running without an explicit `return` value, Python automatically returns `None`.
4. **Placeholder in Automation Scripts:** If you create a variable for a router's IP address before discovering it via LLDP or DNS, you should initialize it as `router_ip = None`.

```python
discovered_neighbor_ip = None
print(type(discovered_neighbor_ip))  # Output: <class 'NoneType'>
print(bool(discovered_neighbor_ip))  # Output: False
```

---

## 4. Working with Files: Reading, Writing, and Appending

In network automation, you constantly interact with files: reading saved CLI outputs (`show_version.txt`), loading lists of target devices, writing configuration backups, or appending results to an audit log.

*(First, let's look at how file operations work at a basic level, and in Section 5 we will upgrade to **Context Managers**, which is the best-practice way to handle files.)*

### Reading from a File (`mode="r"`)
To open a file in your current working directory, use the built-in `open()` function. By default, `open()` opens the file in **read-only text mode (`mode="r"`)** and returns a **file handle** (commonly named `f`).

There are four ways to read content from an open file handle:

#### 1. `.read()` — Read the Entire File into One String
Reads the whole file from start to finish and stores it in a single string (`str`) variable.
```python
f = open("show_version.txt")  # Default mode is "r" (read text)
data = f.read()               # Reads entire file into a single string
f.close()                     # Always close the file when finished!

print(type(data))             # Output: <class 'str'>
```

#### 2. `.readline()` and `.seek(0)` — Read One Line at a Time
Every time you call `f.readline()`, Python reads the next line in the file and moves an internal cursor forward. If you ever need to reset the cursor back to the very beginning of the file without closing and reopening it, use `f.seek(0)`.
```python
f = open("show_version.txt")
first_line = f.readline()     # Reads line 1
second_line = f.readline()    # Reads line 2

f.seek(0)                     # Resets file cursor back to the beginning (byte 0)
f.close()
```

#### 3. `.readlines()` — Read All Lines into a Python List
Notice the **`s`** at the end of `.readlines()`. This method reads the entire file and returns a **list (`list`)**, where each element of the list is one line (`str`) from the file.
```python
f = open("show_version.txt")
lines_list = f.readlines()    # Returns a list of strings
f.close()

print(type(lines_list))       # Output: <class 'list'>
print(len(lines_list))        # Output: 76 (file has 76 lines)
```

#### 4. Looping Directly Over the File Handle (Memory-Efficient)
Instead of loading the whole file into memory at once, you can iterate directly over the file variable `f` using a `for` loop:
```python
f = open("show_version.txt")
for line in f:
    print(line)
f.close()
```

---

### Writing to a File (`mode="w"`)
To write data to a file, call `open()` with **`mode="w"`**.

```python
f = open("router_config.txt", mode="w")
f.write("hostname edge-rtr-01\n")
f.write("ip domain-name netauto.lab\n")
f.flush()  # Forces buffered data out to the OS disk immediately
f.close()  # Closing also flushes and releases the file
```

#### Important Rules When Writing Files (`mode="w"`):
1. **Explicit Newlines (`\n`):** Unlike `print()`, the `.write()` method does **not** automatically add a line break at the end. You must include `\n` at the end of your string if you want a new line.
2. **OS Caching and `.flush()`:** When you run `f.write()`, the operating system often caches (buffers) the data in RAM before writing it to the hard drive. If you inspect the file on disk before closing it, it might look empty (`0` bytes). Calling `f.flush()` or `f.close()` forces the operating system to write the cached data to the file system immediately.
3. **`mode="w"` is DESTRUCTIVE!**  
   > **Warning:** Just like copying a new file over `startup-config` on a router, opening an existing file with `mode="w"` **immediately erases all previous contents** of that file and replaces them with your new data!

---

### Appending to a File (`mode="a"`)
What if you want to add new log entries to the end of an existing file **without** destroying what is already inside? Use **`mode="a"`** (append mode).

```python
# Adds a new line to the very end of the existing file
f = open("audit_log.txt", mode="a")
f.write("2026-10-15: BGP configuration verified on core-rtr-01\n")
f.close()
```

> **Architectural Tip from Kirk Byers:**  
> When working with files in Python, stick to two patterns:
> 1. **Destructive Write (`mode="w"`):** Gather all the data you want in memory and completely write/replace the entire file.
> 2. **Append (`mode="a"`):** Add new lines to the very end of the file.  
> **Never try to insert or edit text in the middle of a file in place.** If you find yourself searching and updating records in the middle of a file repeatedly, you should use a lightweight database (like Python's built-in `sqlite3`) instead of a plain text file!

---

## 5. Python Code Blocks & File Context Managers (`with`)

### An Aside on Python Code Blocks
Before using Context Managers, you need to understand how Python structures **indented code blocks** (used in `with` statements, `if` conditionals, `for` loops, and functions):

1. **The Colon Terminator (`:`):** Every block header line ends with a colon (`:`). The colon tells Python: *"An indented block of code is about to follow."*
2. **4 Spaces of Indentation:** Every line belonging to that block must be indented at the exact same level—always **4 spaces** (never tabs).
3. **Nested Blocks:** You can put a code block inside another code block (for example, a `for` loop inside an `if` statement). Each deeper level adds another 4 spaces (4 spaces, 8 spaces, 12 spaces, etc.).
4. **Ending the Block:** Python does not use `end` keywords or closing curly braces `}`. To end a code block, you simply **stop indenting** (return to the previous margin level).

```python
# Visual structure of Python code blocks
if True:                                  # <-- Colon starts Block Level 1
    print("Connected to router")          # 4 spaces (inside 'if' block)
    for i in range(3):                    # <-- Colon starts Block Level 2
        print("Checking interface", i)    # 8 spaces (inside 'for' block)
    print("Finished interface checks")    # Back to 4 spaces ('for' block ended, still in 'if')

print("Script complete")                  # 0 spaces ('if' block has ended)
```

---

### File Context Managers (`with open(...) as f:`)
In software and network engineering, many operations follow the exact same 3-step lifecycle:
1. **Open** a resource (a file, a database connection, a REST API session, or an SSH/Netmiko session to a router).
2. **Perform operations** on that resource.
3. **Close and clean up** the resource.

Instead of manually calling `f = open(...)` and remembering to type `f.close()`, the canonical (proper Pythonic) way is to use a **Context Manager** via the **`with`** statement:

```python
# Reading a file using a Context Manager (Best Practice)
with open("show_version.txt", mode="r") as f:
    data = f.read()

# As soon as the indentation ends here, Python AUTOMATICALLY closes 'f'!
print(data)
```

#### Why You Should Always Use Context Managers:
1. **Automatic Closing & Flushing:** The moment your code leaves the 4-space indented block, Python automatically calls `f.flush()` (if writing/appending) and `f.close()`.
2. **Guaranteed Cleanup During Crashes (Exceptions):**  
   Imagine your script opens a file (or an SSH session to a Cisco router) without a context manager, and an unexpected error crashes your script on the next line. The `f.close()` line is never reached, leaving unushed files or hung VTY/SSH sessions!  
   **With a Context Manager, cleanup ALWAYS happens.** Even if an unhandled exception crashes your code inside the `with` block, Python guarantees that the file is gracefully flushed and closed before the program exits.

---

## 6. Python Lists: Ordered Collections of Data

### List Basics
A **List (`list`)** is an ordered, sequential collection of elements (similar to an *array* in other programming languages).
- **Syntax:** Created using square brackets `[]` with commas separating each element.
- **Mixed Data Types:** A list can hold any combination of data types (`str`, `int`, `float`, `bool`, `None`, or even other `list`s), although in network automation we usually group similar items together (like a list of VLANs or a list of router IP addresses).
- **Zero-Based Indexing:** Just like interface `GigabitEthernet0/0` starts at `0`, Python lists start counting at **index `0`**.
- **Negative Indexing:** You can count backward from the end of a list! Index **`-1`** always gives you the **very last element**, `-2` gives the second-to-last element, and so on.

```python
# Creating a list of core routers
routers = ["core-rtr-01", "core-rtr-02", "edge-fw-01", "dist-sw-01"]
print(type(routers))  # Output: <class 'list'>

# Accessing elements using zero-based indices
print(routers[0])     # First element: 'core-rtr-01'
print(routers[1])     # Second element: 'core-rtr-02'

# Accessing the last element using negative indices
print(routers[-1])    # Very last element: 'dist-sw-01'
print(routers[-2])    # Second to last element: 'edge-fw-01'

# Updating (reassigning) an element in place
routers[0] = "br-spo-core-01"
print(routers)        # Output: ['br-spo-core-01', 'core-rtr-02', 'edge-fw-01', 'dist-sw-01']
```

---

### Built-in Helpers: `len()`, `range()`, and Membership (`in`)

#### 1. Checking List Length with `len()`
Returns the total number of elements inside the list as an integer.
```python
vlans = [10, 20, 30, 40, 50]
print(len(vlans))  # Output: 5
```

#### 2. Generating Number Sequences with `range()`
The `range()` built-in generates a sequence of numbers dynamically:
- `range(n)`: Starts at `0` by default and goes up to **$n - 1$** (the stopping number is **excluded**). Notice that `range(5)` generates `0, 1, 2, 3, 4`, which matches the exact indices of a 5-element list!
- `range(start, stop)`: Starts at `start` (included) and stops at $\text{stop} - 1$ (`stop` is excluded).

```python
# Generate indices for a 7-element list (0 through 6)
indices = list(range(7))
print(indices)  # Output: [0, 1, 2, 3, 4, 5, 6]

# Networking Use Case: Generate switch access port numbers 1 through 4 (5 is excluded!)
switch_ports = list(range(1, 5))
print(switch_ports)  # Output: [1, 2, 3, 4]
```

#### 3. List Membership Check (`in` Keyword)
How do you check if a specific VLAN or IP address exists inside a list? Use the **`in`** keyword. It returns a Boolean (`True` or `False`).

```python
allowed_vlans = [10, 20, 30, 100, 200]

print(100 in allowed_vlans)  # Output: True
print(999 in allowed_vlans)  # Output: False
```
*(Note: Lists can contain duplicate elements. The `in` check does not count how many times an item appears; it simply answers "Does this item exist anywhere in the list? Yes or No.")*

---

### Essential List Methods
List methods are actions you call directly on a list object using dot notation (`my_list.method()`).

```python
# Starting list of DNS servers
dns_servers = ["8.8.8.8", "1.1.1.1"]

# 1. append() - Most common method! Adds ONE element to the very end of the list (in place)
dns_servers.append("9.9.9.9")
print(dns_servers)  # Output: ['8.8.8.8', '1.1.1.1', '9.9.9.9']

# 2. pop() - Second most common! Removes and returns an element from the list
# Default pop() with no argument removes and returns the VERY LAST element:
last_dns = dns_servers.pop()
print(last_dns)     # Output: '9.9.9.9'
print(dns_servers)  # Output: ['8.8.8.8', '1.1.1.1']

# pop(0) removes and returns the VERY FIRST element (index 0):
first_dns = dns_servers.pop(0)
print(first_dns)    # Output: '8.8.8.8'
print(dns_servers)  # Output: ['1.1.1.1']

# 3. extend() - Appends multiple elements from another list in place
backup_dns = ["208.67.222.222", "208.67.220.220"]
dns_servers.extend(backup_dns)
print(dns_servers)  # Output: ['1.1.1.1', '208.67.222.222', '208.67.220.220']

# 4. List Concatenation (+) - Creates a brand-new combined list
all_dns = dns_servers + ["4.2.2.1", "4.2.2.2"]

# 5. count() - Counts how many times a value appears in the list
print(all_dns.count("1.1.1.1"))  # Output: 1

# 6. copy() - Creates a shallow copy of the list
dns_backup_copy = all_dns.copy()

# 7. clear() - Empties the list (though reassigning `dns_servers = []` is clearer)
dns_servers.clear()
```
*(Python also includes methods like `.sort()` to sort elements and `.reverse()` to reverse the order of a list in place.)*

---

### List Slices (`my_list[start:stop]`)
**List slicing** allows you to dynamically extract a subset of elements from a list to create a new list.

- **Syntax:** `my_list[start:stop]`
- **`start` index is INCLUDED.**
- **`stop` index is EXCLUDED** (stops at $\text{stop} - 1$).
- **Non-Destructive:** Slicing **never modifies the original list**; it returns a brand-new list.

| Slice Syntax | Behavior | Example on `["rtr1", "rtr2", "rtr3", "fw1", "sw1"]` |
| :--- | :--- | :--- |
| `my_list[1:3]` | Starts at index `1`, stops before index `3` (gets indices `1` and `2`). | `["rtr2", "rtr3"]` |
| `my_list[:3]` | No `start` specified: starts at the very beginning (`0`) up to index `2`. | `["rtr1", "rtr2", "rtr3"]` |
| `my_list[3:]` | No `stop` specified: starts at index `3` and goes all the way to the end. | `["fw1", "sw1"]` |
| `my_list[:]` | Neither `start` nor `stop`: copies the entire list (shallow copy). | `["rtr1", "rtr2", "rtr3", "fw1", "sw1"]` |
| `my_list[2:-1]` | Starts at index `2` and stops right before the last element (`-1` excluded). | `["rtr3", "fw1"]` |

```python
# Practical Slicing Example: Extracting header lines vs. interface lines
cli_lines = [
    "Interface          IP-Address      OK? Method Status",
    "GigabitEthernet0/0 10.1.1.1        YES NVRAM  up",
    "GigabitEthernet0/1 10.2.2.1        YES NVRAM  up",
    "Loopback0          192.168.0.1     YES NVRAM  up",
    "rtr-core-01#"
]

# Skip line 0 (header) and exclude the last line (-1, router prompt)
interface_lines = cli_lines[1:-1]
print(interface_lines)
```

---

### Multidimensional Lists (Lists Within Lists)
A list can contain other lists as its elements. In network automation, this happens frequently when you group devices by Data Center site or parse tabular CLI output into rows and columns.

To access elements inside a multidimensional list, **chain your square bracket indices from left to right**:
1. The first bracket `[i]` selects the element from the **outer list**.
2. The second bracket `[j]` selects the element from the **inner list**.

```python
# Outer list containing two inner lists: [VLAN_IDs, Datacenter_Names]
network_matrix = [
    [10, 20, 30],           # Element 0 of outer list
    ["SF_DC1", "LA_DC2"]    # Element 1 of outer list
]

# 1. Access the first inner list
print(network_matrix[0])       # Output: [10, 20, 30]

# 2. Chain indices to get the second item (index 1) of the first inner list (index 0)
print(network_matrix[0][1])    # Output: 20

# 3. Chain indices to get "LA_DC2" (outer index 1, inner index 1)
print(network_matrix[1][1])    # Output: 'LA_DC2'
```

---

## 7. Under the Hood: Mutable vs. Immutable Objects & Copying

*(Note: As Kirk Byers mentions, this section covers an intermediate topic. Understanding how Python handles memory will save you from painful bugs when manipulating device dictionaries and lists later on!)*

### Variable Names vs. Objects in Memory (`id()` and `is`)
When you write `router1_addr = "10.1.1.1"`, Python does two separate things:
1. It allocates space in your computer's **memory (RAM)** to store the string object `"10.1.1.1"`.
2. It creates a **variable name (tag)** called `router1_addr` that **points** to that object in memory.

If you then write `gw1 = router1_addr`, Python does **not** create a second copy of `"10.1.1.1"`. Instead, it attaches a second name tag (`gw1`) pointing to the **exact same object in memory**!

- **`id(var)`:** Returns the unique memory identifier (address) of the object that `var` points to.
- **`==` vs. `is`:**
  - `a == b` checks **Equality**: *"Do these two variables contain the same value?"*
  - `a is b` checks **Identity**: *"Do these two variable names point to the exact same object in memory (`id(a) == id(b)`)?"*

```python
router1_addr = "10.1.1.1"
gw1 = router1_addr

# Both names point to the exact same memory address
print(id(router1_addr))      # Example Output: 14023489120
print(id(gw1))               # Example Output: 14023489120
print(router1_addr is gw1)   # Output: True
```

---

### Immutable Objects (Cannot Be Changed in Memory)
An **immutable object** is an object whose value in memory **can never be modified** after it is created.

**Which Python types are Immutable?**
- `None`
- Booleans (`True`, `False`)
- Integers (`int`) and Floats (`float`)
- Strings (`str`)
- Tuples (`tuple`)

*"Wait—if integers are immutable, why can I run `ssh_timeout = 20` and then change it to `ssh_timeout = 10` or `ssh_timeout += 1`?"*  
Because you are **not modifying the number `20` in memory!** Instead, Python creates a **brand-new integer object** (`10` or `21`) at a new memory location and moves the name tag `ssh_timeout` to point to that new object:

```python
ssh_timeout = 20
print(id(ssh_timeout))  # Memory ID of integer object 20 (e.g., 4300100)

ssh_timeout += 1        # Creates a NEW integer object 21 in memory and moves the pointer!
print(id(ssh_timeout))  # Different Memory ID! (e.g., 4300132)
```

---

### Mutable Objects (Can Be Modified in Place)
A **mutable object** is an object whose contents **can be changed directly in memory** without creating a new object or changing its `id()`.

**Which Python types are Mutable?**
- **Lists (`list`)**
- **Dictionaries (`dict`)** *(covered later)*
- **Sets (`set`)** *(covered later)*

```python
datacenters = ["sf1", "sf2", "la1"]
print(id(datacenters))       # Memory ID: e.g., 14055599900

# Modify the list in place using append()
datacenters.append("dallas1")
print(id(datacenters))       # Exact SAME Memory ID: 14055599900!
```

#### The Mutable Aliasing Trap!
Because lists are mutable, look at what happens when you assign `my_dcs = datacenters` without copying:

```python
datacenters = ["sf1", "sf2", "la1"]
my_dcs = datacenters          # DANGER: Both names point to the SAME list in memory!

my_dcs.append("london1")      # We think we are only modifying 'my_dcs'...

print(my_dcs)                 # Output: ['sf1', 'sf2', 'la1', 'london1']
print(datacenters)            # Output: ['sf1', 'sf2', 'la1', 'london1'] -> ALSO MODIFIED!
```

To create two independent flat lists, use `.copy()` (which performs a **shallow copy**):
```python
datacenters = ["sf1", "sf2", "la1"]
my_dcs = datacenters.copy()   # Creates a new outer list in memory

my_dcs.append("london1")
print(my_dcs)                 # Output: ['sf1', 'sf2', 'la1', 'london1']
print(datacenters)            # Output: ['sf1', 'sf2', 'la1'] (Unchanged!)
```

---

### Shallow Copy vs. Deep Copy (`copy.deepcopy()`)
Internally, a Python list does not store objects directly inside a block of memory; it stores **pointers (references)** to those objects.

#### 1. When a Shallow Copy (`.copy()`) is Fine
If your list only contains **immutable** elements (like strings or integers: `["sf1", "sf2", "dallas"]`), a shallow copy (`dc_list = datacenters.copy()`) is completely safe. Even though both lists initially point to the same string objects in memory, strings are immutable—reassigning `dc_list[-1] = "denver"` simply points that slot to a new string without affecting `datacenters`.

#### 2. When a Shallow Copy Fails (Nested Mutable Structures)
What if you have a **list of lists** (a multidimensional list where the inner elements are **mutable**)?
- **A Shallow Copy (`.copy()`) ONLY copies the outermost list container.**
- The pointers inside the new outer list still point to the **exact same inner lists** in memory!

```python
# Multidimensional list: [ [SF Data Center IPs], [LA Data Center IPs] ]
datacenters = [
    ["10.1.1.1", "10.1.1.2"],  # Inner list 0 (SF)
    ["10.2.2.1", "10.2.2.2"]   # Inner list 1 (LA)
]

# Shallow copy only duplicates the outer container!
dc_list = datacenters.copy()

# Look: Both outer lists share the EXACT SAME inner list at index 0!
print(dc_list[0] is datacenters[0])  # Output: True!

# If we append a new IP to the inner SF list via 'dc_list'...
dc_list[0].append("10.1.1.99")

# ...it modifies BOTH variables because there is really only ONE inner SF list!
print(dc_list[0])      # Output: ['10.1.1.1', '10.1.1.2', '10.1.1.99']
print(datacenters[0])  # Output: ['10.1.1.1', '10.1.1.2', '10.1.1.99'] -> BUG!
```

#### 3. The Solution: Deep Copy (`copy.deepcopy()`)
To copy a nested data structure (like a list of lists, or a list of dictionaries from a network API) so that **every level of mutable objects** gets its own independent copy in memory, import the built-in `copy` module and use **`copy.deepcopy()`**:

```python
import copy

datacenters = [
    ["10.1.1.1", "10.1.1.2"],
    ["10.2.2.1", "10.2.2.2"]
]

# Deep copy traverses all levels and copies every mutable object!
dc_list = copy.deepcopy(datacenters)

print(dc_list[0] is datacenters[0])  # Output: False (Completely independent inner lists!)

# Modifying the inner list in 'dc_list' no longer affects 'datacenters'
dc_list[0].append("10.1.1.99")

print(dc_list[0])      # Output: ['10.1.1.1', '10.1.1.2', '10.1.1.99']
print(datacenters[0])  # Output: ['10.1.1.1', '10.1.1.2'] (Safely untouched!)
```
*(Note: Because `copy.deepcopy()` traverses the entire data structure and duplicates every mutable object, it can use more CPU and memory if your data structure has millions of elements.)*

---

## 8. Tuples: Immutable Lists

### What is a Tuple (`tuple`)?
A **Tuple** is simply an **immutable list**—an ordered sequence of elements that **cannot be modified** once it is created.

- **Creation Syntax:** Use **parentheses `()`** instead of square brackets `[]`, with elements separated by commas.
- **Accessing Elements:** Just like a list, you access elements or slices using **square brackets `[]`** and zero-based indices (`my_tuple[0]`).
- **No Modification Allowed:** You **cannot** reassign elements (`my_tuple[0] = "new"` causes a `TypeError`), and tuples do **not** have `.append()`, `.extend()`, or `.pop()` methods.

```python
# Creating a tuple representing a fixed network device record (Hostname, IP, SSH Port)
device_record = ("core-rtr-01", "10.254.0.1", 22)
print(type(device_record))  # Output: <class 'tuple'>

# Accessing elements works just like a list (using square brackets!)
print(device_record[0])     # Output: 'core-rtr-01'
print(device_record[-1])    # Output: 22

# Trying to modify a tuple raises a TypeError!
# device_record[1] = "10.254.0.2"  --> TypeError: 'tuple' object does not support item assignment
```

### Why Do Network Engineers Need Tuples?
1. **Reading Other People's Code & Libraries:** Many built-in Python functions and networking libraries return multiple values packaged together as a `tuple`.
2. **Protecting Constant Sequences:** If you have a collection of values that should never change during script execution (such as `(hostname, management_ip, vendor)`), storing them in a tuple prevents accidental modification.

### The Classic Tuple "Gotcha": Accidental Commas!
In Python, it is actually the **comma (`,`)**—not the parentheses—that tells Python to create a tuple! If you accidentally leave a comma at the end of a line or between two strings without brackets, Python will quietly create a `tuple` instead of a `str`.

```python
# Standard tuple with parentheses
ips_tuple1 = ("10.1.1.1", "10.1.1.2")

# GOTCHA 1: No parentheses, just a comma -> Still creates a tuple!
ips_tuple2 = "10.1.1.1", "10.1.1.2"
print(type(ips_tuple2))  # Output: <class 'tuple'>

# GOTCHA 2: Accidental trailing comma when defining a string variable!
my_router_ip = "10.1.1.1",
print(type(my_router_ip))  # Output: <class 'tuple'> (NOT a string! Will break Netmiko if passed as an IP!)
print(my_router_ip)        # Output: ('10.1.1.1',)
```
> **Troubleshooting Tip:** If your network automation script throws an error like `AttributeError: 'tuple' object has no attribute 'split'`, check your variable assignments—you probably left an accidental comma at the end of a line!

---

## 9. Hands-On Practice: Week 2 Lab Exercises

Try these four hands-on exercises to practice treating network data systematically using Week 2 concepts.

### Exercise 1: Subnet Calculator & VLAN Load Balancer (Numbers & Booleans)
Write a short script `subnet_vlan_calc.py` that:
1. Calculates the number of usable hosts in a `/26` IPv4 network ($32 - 26 = 6$ host bits; usable hosts $= 2^6 - 2$).
2. Calculates link utilization percentage for a $10\text{ Gbps}$ interface carrying $3.333\text{ Gbps}$ of traffic (`(3.333 / 10) * 100`) and rounds it to **2 decimal places** using `round()`.
3. Checks whether `vlan_id = 204` is an even VLAN using the modulo operator (`%`).

**Example Solution (`subnet_vlan_calc.py`):**
```python
#!/usr/bin/env python

# 1. Calculate usable hosts in a /26 subnet (6 host bits)
host_bits = 6
usable_hosts = (2 ** host_bits) - 2
print("Usable hosts in /26:", usable_hosts)  # 62

# 2. Calculate and round link utilization percentage
traffic_gbps = 3.333
capacity_gbps = 10
utilization_pct = round((traffic_gbps / capacity_gbps) * 100, 2)
print("Link Utilization (%):", utilization_pct)  # 33.33

# 3. Check if VLAN 204 is even (remainder of division by 2 is 0)
vlan_id = 204
is_even_vlan = (vlan_id % 2) == 0
print("Is VLAN 204 even?", is_even_vlan)  # True
```

---

### Exercise 2: Processing CLI Output with Context Managers and List Slices
Imagine you have a text file named `show_ip_int_brief.txt` with the following 6 lines:
```text
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     10.10.1.1       YES NVRAM  up                    up      
GigabitEthernet0/1     10.10.2.1       YES NVRAM  up                    up      
GigabitEthernet0/2     unassigned      YES NVRAM  administratively down down    
Loopback0              172.16.0.1      YES NVRAM  up                    up      
core-rtr-01#
```

Write a script `parse_interfaces.py` that:
1. Uses a **`with` context manager** to create `show_ip_int_brief.txt` (using `mode="w"`).
2. Re-opens `show_ip_int_brief.txt` using a **`with` context manager** in read mode and reads all lines into a list using `.readlines()`.
3. Uses **list slicing** to remove the first line (the table header at index `0`) and the very last line (the router prompt at index `-1`).
4. Prints the number of actual interface lines using `len()`, and writes those interface lines to a new file `clean_interfaces.txt`.

**Example Solution (`parse_interfaces.py`):**
```python
#!/usr/bin/env python

# Step 1: Create the sample CLI output file safely using a context manager
with open("show_ip_int_brief.txt", mode="w") as f:
    f.write("Interface              IP-Address      OK? Method Status                Protocol\n")
    f.write("GigabitEthernet0/0     10.10.1.1       YES NVRAM  up                    up\n")
    f.write("GigabitEthernet0/1     10.10.2.1       YES NVRAM  up                    up\n")
    f.write("GigabitEthernet0/2     unassigned      YES NVRAM  administratively down down\n")
    f.write("Loopback0              172.16.0.1      YES NVRAM  up                    up\n")
    f.write("core-rtr-01#\n")

# Step 2: Read all lines into a list using a context manager
with open("show_ip_int_brief.txt", mode="r") as f:
    all_lines = f.readlines()

# Step 3: Slice the list from index 1 up to (but excluding) the last line (-1)
interface_lines = all_lines[1:-1]

print("Total interface lines extracted:", len(interface_lines))
print("First interface line:", interface_lines[0])
print("Last interface line:", interface_lines[-1])
```

---

### Exercise 3: List Manipulation (`append`, `extend`, `pop`, `in`)
In IPython or a script:
1. Create a list of VLANs: `vlans = [10, 20, 30]`.
2. Use `.append()` to add VLAN `40`.
3. Use `.extend()` to add `[100, 200]` to the list.
4. Check if VLAN `100` is in your list using `in`.
5. Remove and capture the very first VLAN (`10`) using `.pop(0)` and the very last VLAN (`200`) using `.pop()`.

**Example Solution:**
```python
vlans = [10, 20, 30]
vlans.append(40)              # [10, 20, 30, 40]
vlans.extend([100, 200])      # [10, 20, 30, 40, 100, 200]

print(100 in vlans)           # True

first_vlan = vlans.pop(0)     # Removes 10
last_vlan = vlans.pop()       # Removes 200

print("Removed first:", first_vlan)  # 10
print("Removed last:", last_vlan)    # 200
print("Remaining VLANs:", vlans)     # [20, 30, 40, 100]
```

---

### Exercise 4: Spot the Memory Bug (Shallow Copy vs. Deep Copy)
A network engineer wrote the code below to create a backup copy of a nested firewall rule table before adding a temporary rule to `candidate_rules`. Why did `production_rules` also get modified, and how do you fix it?

```python
# Broken Code:
production_rules = [
    ["permit", "tcp", "10.0.0.0/8", "eq 443"],
    ["deny", "ip", "any", "any"]
]

candidate_rules = production_rules.copy()
candidate_rules[0].append("log")

print("Production:", production_rules[0])
# Output: ['permit', 'tcp', '10.0.0.0/8', 'eq 443', 'log']  <-- OOPS!
```

**Answer & Fix:**  
`production_rules` is a **multidimensional list** (a list containing inner mutable lists). Calling `.copy()` performs a **shallow copy**, which only duplicates the outer container while keeping pointers to the exact same inner lists!  
To fix it, import `copy` and use **`copy.deepcopy(production_rules)`**:

```python
import copy

production_rules = [
    ["permit", "tcp", "10.0.0.0/8", "eq 443"],
    ["deny", "ip", "any", "any"]
]

# Fix: Use deepcopy so inner lists are also duplicated independently
candidate_rules = copy.deepcopy(production_rules)
candidate_rules[0].append("log")

print("Production:", production_rules[0])  # ['permit', 'tcp', '10.0.0.0/8', 'eq 443']
print("Candidate: ", candidate_rules[0])   # ['permit', 'tcp', '10.0.0.0/8', 'eq 443', 'log']
```

---

## 10. Quick Reference Cheat Sheet (Week 2)

| Category | Operation / Concept | Python Syntax | Key Behavior for Network Engineers |
| :--- | :--- | :--- | :--- |
| **Numbers** | Standard Division | `10 / 2` | Always returns a `float` (`5.0`). |
| **Numbers** | Modulo (Remainder) | `vlan % 2` | Returns division remainder (`0` = even, `1` = odd). |
| **Numbers** | Power / Exponent | `2 ** 8` | Calculates $2^8 = 256$ (great for subnetting). |
| **Numbers** | Round Float | `round(val, 2)` | Rounds a float to `2` decimal places. |
| **Numbers** | Increment / Decrement | `i += 1` / `i -= 1` | Shorthand for `i = i + 1` and `i = i - 1`. |
| **Booleans** | Logical Operators | `and`, `or`, `not` | Combine or invert boolean expressions. |
| **Booleans** | Falsy (Evaluates `False`) | `""`, `0`, `0.0`, `[]`, `{}`, `None` | All other strings, numbers, and non-empty lists are `True`. |
| **NoneType** | Null / Empty Value | `my_var = None` | Special type; default return of functions; `False` in bool context. |
| **Files** | Context Manager (Read) | `with open("f.txt") as f:` | Automatically closes file when indented block ends. |
| **Files** | Read Methods | `f.read()` / `f.readlines()` | `.read()` returns one `str`; `.readlines()` returns a `list` of lines. |
| **Files** | Write vs. Append | `mode="w"` vs. `mode="a"` | `"w"` overwrites/destroys existing file; `"a"` appends to the end. |
| **Lists** | Indexing | `my_list[0]` / `my_list[-1]` | `0` is the first item; `-1` is the very last item. |
| **Lists** | Length & Membership | `len(my_list)` / `x in my_list` | Returns item count (`int`) / checks if `x` is in list (`bool`). |
| **Lists** | Generate Sequence | `range(1, 5)` | Generates `1, 2, 3, 4` (`start` included, `stop` excluded). |
| **Lists** | Add Elements | `.append(x)` / `.extend(lst)` | `.append()` adds 1 item to end; `.extend()` adds items from a list. |
| **Lists** | Remove & Return | `.pop()` / `.pop(0)` | `.pop()` removes last item; `.pop(0)` removes first item. |
| **Lists** | Slicing | `my_list[1:4]` | Extracts indices `1, 2, 3` (`4` is excluded); does not modify original. |
| **Lists** | Multidimensional Access | `matrix[0][1]` | Chains indices left-to-right (outer list `0`, inner list `1`). |
| **Memory** | Identity Check | `id(a)` / `a is b` | Checks if two names point to the exact same object in RAM. |
| **Memory** | Immutable Types | `int`, `float`, `str`, `bool`, `None`, `tuple` | Cannot be changed in place; reassignment creates a new object. |
| **Memory** | Mutable Types | `list`, `dict`, `set` | Modified in place; assigning `b = a` aliases the same object! |
| **Memory** | Shallow vs. Deep Copy | `lst.copy()` vs. `copy.deepcopy(lst)` | Use `deepcopy()` when copying nested lists/dicts! |
| **Tuples** | Immutable Sequence | `t = ("rtr1", "10.0.0.1")` | Uses `()`; accessed with `t[0]`; cannot be modified; watch out for stray commas! |