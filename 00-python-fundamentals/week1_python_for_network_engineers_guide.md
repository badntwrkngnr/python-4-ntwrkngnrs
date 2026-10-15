# Learning Python for Network Engineers — Week 1 Study Guide
**Course Reference:** Kirk Byers (*Learning Python for Network Engineers* / [twin-bridges/learning_python](https://github.com/twin-bridges/learning_python))  
**Target Audience:** Network Engineers transitioning to Network Automation  
**Language Level:** English (B1/B2 Intermediate)

---

## 1. Introduction: Thinking of the Network as a System

As a network engineer, you already know how to configure routers, switches, and firewalls using the Command Line Interface (CLI). However, configuring devices one by one ("box-by-box") does not scale when you manage dozens or hundreds of nodes. 

When you learn **Python**, you change your perspective: instead of treating each router as an isolated box, you start **treating the network as an integrated system**.

### Why Python Dominates Network Automation
Over the last decade, Python has become the main programming language for network automation (alongside frameworks like **Ansible**). Here is why Python is the best choice if you do not have a coding background:

1. **High-Level and Readable:** You do not need to manage complex computer memory or low-level hardware details. Python syntax looks very close to plain English.
2. **Massive Networking Ecosystem:** You do not have to build everything from scratch. Kirk Byers and the networking community have created powerful open-source libraries specifically for network engineers:
   - **Netmiko:** Simplifies SSH connections to network devices (Cisco IOS, Juniper Junos, Arista EOS, Huawei VRP, Nokia SR OS, etc.).
   - **NAPALM:** Provides a unified way to retrieve operational data and manage configurations across different vendors.
   - **Nornir:** A pure-Python automation framework that executes tasks across your network inventory in parallel.
3. **Cross-Platform:** Python runs everywhere—Linux, macOS, and Windows.
4. **Scales with Your Skills:** You can start today with a 5-line script that collects IP addresses, and later build full observability pipelines, configuration compliance tools, or API integrations.

---

## 2. Isolated Environments: Virtual Environments (`venv`) & `pip`

### The Networking Analogy: Virtual Environments are like VRFs
In networking, if you put all customer routes into the `global` routing table, routes can conflict and break the whole router. To solve this, you create **VRFs (Virtual Routing and Forwarding)** or **VLANs** to isolate traffic.

In Python, your operating system (especially Linux) already uses a "system Python" for internal OS tools. If you install or upgrade automation libraries globally, you might accidentally break your operating system or create version conflicts between two different scripts.

A **Python Virtual Environment (`venv`)** is an **isolated sandbox** (just like a VRF):
- Project A can have its own `venv` with a specific version of the `requests` library to talk to a REST API.
- Project B can have a separate `venv` with a specific version of `netmiko` to configure legacy switches.
- Neither environment affects the other or the base operating system.

### How to Create and Activate a Virtual Environment

#### On Linux / macOS
```bash
# 1. Create the virtual environment using the 'venv' module (-m)
python3.11 -m venv py311_venv

# 2. Activate the virtual environment
source py311_venv/bin/activate

# Notice how your terminal prompt changes to show the active environment:
# (py311_venv) netadmin@linux-jumpbox:~$
```

#### On Windows
On Windows, Python includes a convenient launcher command called `py`:
```cmd
:: 1. Check your Python version
py

:: 2. Create the virtual environment
py -m venv py311_venv

:: 3. Activate the virtual environment
py311_venv\Scripts\activate

:: Your prompt will now show (py311_venv)
```

---

### Managing Packages with `pip`
Once your virtual environment is active, you use **`pip`** (Python's package installer) to install external libraries.

> **Best Practice Tip:** Always run `python -m pip` instead of just `pip`. Sometimes your system has multiple Python versions installed. Using `python -m pip` guarantees that you are installing packages into the exact Python interpreter you are currently running.

```bash
# Check which packages are currently installed in your sandbox
python -m pip list

# Upgrade pip to a specific or latest version
python -m pip install --upgrade pip
# Or specify an exact version:
python -m pip install pip==24.0
```

#### Installing Course Dependencies (`requirements.txt`)
In real-world network automation projects (and in the `twin-bridges/learning_python` repository), engineers list all required libraries inside a text file named **`requirements.txt`**. This ensures every engineer on the team uses the exact same tools.

```bash
# Clone the course repository
git clone https://github.com/twin-bridges/learning_python.git
cd learning_python

# Install all required libraries automatically
python -m pip install -r requirements.txt
```

---

## 3. The Interactive Shell (REPL) and IPython

Before writing a full script file, network engineers often want to test a quick command to see how Python behaves. You can do this in the **Python Interpreter Shell** (also called **REPL**: *Read-Eval-Print Loop*).

### The Networking Analogy: Live Router CLI vs. Configuration File
- **The Interpreter Shell (IPython)** is like typing `show ip interface brief` directly into a router's CLI: you type a command, hit `Enter`, and immediately see the output.
- **A Python Script (`.py` file)** is like preparing a full configuration template in a text file and pushing it to the device.

### Using IPython
Instead of the basic default Python shell, Kirk Byers recommends **IPython** (*Interactive Python*), which provides syntax highlighting, better error messages, and easier inspection.

```bash
# Launch IPython from your terminal
python -m IPython
```

Inside IPython, you can test expressions immediately:
```python
In [1]: ip_addr = "10.254.0.1"

In [2]: print(ip_addr)
10.254.0.1

In [3]: type(ip_addr)
Out[3]: str
```

### Fixing IPython's Intrusive Autocomplete
Newer versions of IPython include an aggressive inline autocomplete feature that often gets in the way when you are typing code. You can disable it by creating an IPython configuration file:

1. **Generate the default config (if it does not exist):**
   ```bash
   ipython profile create
   ```
2. **Locate the configuration file:**
   - **Linux/macOS:** `~/.ipython/profile_default/ipython_config.py`
   - **Windows:** `C:\Users\<YourUsername>\.ipython\profile_default\ipython_config.py`
3. **Add these two lines to the file to turn off the annoying autocomplete:**
   ```python
   c.TerminalInteractiveShell.autosuggestions_provider = None
   c.Completer.use_jedi = False
   ```

---

## 4. Python Syntax Fundamentals: Indentation and PEP 8

Every network protocol (like OSPF or BGP) has strict RFC standards so routers from different vendors can communicate. Similarly, Python has a style standard called **PEP 8** (*Python Enhancement Proposal 8*).

### Indentation Defines Code Blocks
Many programming languages (like C, Java, or Go) use curly braces `{ }` to group blocks of code. **Python does not use curly braces.** Instead, Python uses **indentation** (empty spaces at the beginning of a line) to know which lines belong together.

*(Look at how similar this is to a Cisco IOS configuration where sub-commands under `interface GigabitEthernet0/0` or `router ospf 1` are indented!)*

### The Golden Rule: 4 Spaces, NEVER Tabs
When indenting code in Python:
1. **Always use spaces, never the `Tab` character.** Mixing tabs and spaces will cause syntax errors (`TabError`) and break your scripts when sharing code with teammates.
2. **Use exactly 4 spaces per indentation level.**
3. Configure your text editor (VS Code, Vim, Notepad++, etc.) so that pressing the `Tab` key automatically inserts **4 spaces**.

```python
# Example of 4-space indentation in Python (preview of conditional blocks)
bgp_state = "Established"

if bgp_state == "Established":
    print("BGP neighbor is UP.")
    print("Routes are being exchanged.")
```

> **What is a Linter?**  
> In the videos, you will hear the term **linter** (such as `flake8`, `black`, or `ruff`). A linter is an automated tool that checks your Python code to verify if you followed PEP 8 formatting rules and warns you about potential mistakes before you even run the script.

---

## 5. Variables and Naming Conventions

### What is a Variable?
Think of a variable as a **labeled box** (or like an **alias / host-macro** on a network device) where you store data in memory so you can use it later in your script.

To store data in a variable, you use the single equal sign (`=`), which is called the **assignment operator**.

```python
# Assigning network data to variables
hostname = "core-rtr-01"          # String (text)
management_ip = "192.168.100.1"   # String (text)
ospf_process_id = 10              # Integer (whole number)
global_delay_factor = 2           # Integer (used in Netmiko for slow links)
```

> **Important Note for Beginners:**  
> In Python, a single equal sign `=` does **not** mean "is equal to" in the mathematical sense. It means **"take the value on the right and store it inside the variable name on the left."**

### Variable Naming Rules (Enforced by Python)
If you break these rules, Python will stop and give you a `SyntaxError`:
1. You can only use **letters** (`a-z`, `A-Z`), **numbers** (`0-9`), and the **underscore** character (`_`).
2. You **cannot** use hyphens (`-`), spaces, or special symbols like `$` or `@`.
   - *Common Network Engineer Mistake:* In CLI configs or DNS, we love hyphens (`core-rtr-01`). In Python variable names, `core-rtr-01 = "10.0.0.1"` fails because Python interprets `-` as subtraction (minus)! Always use underscores instead: `core_rtr_01`.
3. A variable name **cannot start with a number**.
   - `sfdc_server9 = "172.16.1.9"` -> **Valid** (number is not at the start).
   - `9sfdc_server = "172.16.1.9"` -> **Invalid** (`SyntaxError`).

### Python Naming Conventions (PEP 8 Community Standards)
Python will not crash if you ignore conventions, but following them makes your code **"Pythonic"** (easy for other network automation engineers to read):

| Element Type | Convention Style | Network Automation Examples | Explanation |
| :--- | :--- | :--- | :--- |
| **Variables** | `snake_case` | `my_ip_addr`, `vlan_id`, `bgp_asn` | All lowercase letters with underscores separating words. |
| **Functions** | `snake_case` | `get_bgp_neighbors()`, `send_config()` | Same as variables: lowercase with underscores. |
| **Constants** | `UPPER_SNAKE_CASE` | `DEFAULT_SSH_PORT = 22`, `MAX_TIMEOUT = 60` | Values that should never change during script execution. |
| **Classes** | `PascalCase` | `CiscoIosSSH`, `NetworkDevice` | First letter of every word is capitalized, no underscores. |

### Special Underscore Variables in Python
During the course, you will see underscores used in special ways:

1. **Single Underscore (`_`):**  
   It is a completely valid variable name! By convention, engineers use `_` as a **throwaway (junk) variable** when they need to capture a piece of data they do not care about. A great advantage is that code linters know `_` is intentional and will not complain about an "unused variable."
   ```python
   # Example: Unpacking an interface string where we only want the interface number
   # (Preview of advanced usage)
   _, interface_num = "GigabitEthernet 0/1".split()
   ```

2. **Single Leading Underscore (`_private_var`):**  
   Indicates an **internal or private** variable/function inside a library (like Netmiko). It is a polite warning from the author: *"Do not modify or call this directly in your script unless you really know what you are doing."*

3. **Double Leading and Trailing Underscores (`__name__`):**  
   Called **"Dunder"** (*Double UNDERscore*) or **Magic** variables/methods. These are reserved by Python for internal mechanics (like `__name__` or `__init__`). **Never invent your own `__variable__` names.**

4. **Double Leading Underscore (`__mangled`):**  
   Used internally inside advanced object-oriented classes for "name mangling." As Kirk notes, you will almost never need this in network automation—just stay clear of it.

---

## 6. Standard Input (`input`) and Standard Output (`print`)

To make useful scripts, your program needs a way to talk to the user (displaying status messages or asking for device information).

### Printing to Standard Output (`stdout`) with `print()`
The built-in `print()` function sends text or variable values directly to your terminal screen.

```python
# Printing literal strings and integers
print("Starting OSPF configuration check...")
print(65001)

# Printing variables
device_ip = "10.10.20.1"
print(device_ip)

# Printing multiple items together
print("Connecting to router at IP:", device_ip)
```

### Collecting User Input (`stdin`) with `input()`
Sometimes you do not want to hardcode an IP address or VLAN ID inside your script; instead, you want the script to pause and ask the engineer running it to type the value in the terminal. You do this with the built-in `input()` function.

```python
# The script displays the prompt and waits for the user to type and press Enter
my_ip_addr = input("Please enter the router IP address: ")

print("You entered:", my_ip_addr)
```

> **CRITICAL RULE ABOUT `input()`:**  
> Everything returned by `input()` comes into Python as a **String (`str`)**, even if the user types numbers!  
> For example, if you ask `vlan = input("Enter VLAN ID: ")` and the user types `100`, Python stores it as the text `"100"`, not the number `100`.
> ```python
> vlan_id = input("Enter VLAN ID: ")   # User types: 100
> print(type(vlan_id))                 # Output: <class 'str'>
> ```

---

## 7. Creating and Executing Python Scripts

Interactive shells (`IPython`) are great for testing, but nothing is saved when you close the window. To build repeatable automation tools, you save your code in a plain text file ending with the **`.py`** extension (for example, `my_code.py`).

### Step 1: Write a Simple Script (`my_code.py`)
```python
#!/usr/bin/env python
my_ip_addr = input("Enter an IP address: ")
print(my_ip_addr)
```

### Step 2: How to Execute Your Script

Before running any script, **always verify that your virtual environment (`venv`) is active!**

#### Method A: Calling the Python Interpreter Explicitly (Linux, macOS, Windows)
This is the most common way to run a script:
```bash
# On Linux or macOS (with active venv)
python my_code.py

# On Windows (using python or the py launcher)
python my_code.py
# OR
py my_code.py
```

#### Method B: Direct Execution on Linux / macOS (The Shebang & Permissions)
On Linux systems (like an automation jump-host or Ubuntu server), you can make your `.py` script behave just like a native Linux command or Bash script so you can run `./my_code.py` directly without typing `python` first.

To do this, you need two things:

1. **The Shebang Line (`#!/usr/bin/env python`):**  
   Put this on the **very first line** of your script.  
   - Why use `/usr/bin/env python` instead of `/usr/bin/python`?  
   - Because `env` searches your current Linux `PATH` variable. If your virtual environment (`venv`) is active, `/usr/bin/env python` automatically uses your **virtual environment's Python** (where Netmiko and your libraries are installed) instead of the base operating system's Python!

2. **Executable File Permissions (`chmod`):**  
   By default, new text files in Linux do not have permission to execute as programs. Use `chmod` to add the executable (`+x`) flag:
   ```bash
   # Check current permissions
   ls -l my_code.py
   # -rw-r--r-- 1 netadmin netadmin 88 Oct 15 10:00 my_code.py

   # Add executable permission
   chmod +x my_code.py
   # (Or chmod 755 my_code.py)

   # Verify permissions now show 'x'
   ls -l my_code.py
   # -rwxr-xr-x 1 netadmin netadmin 88 Oct 15 10:00 my_code.py

   # Execute the script directly!
   ./my_code.py
   ```

---

## 8. Hands-On Practice: Week 1 Lab Exercises

To consolidate what you learned in Week 1, try completing these three practical exercises in your lab environment.

### Exercise 1: Environment & IPython Exploration
1. Create a virtual environment named `netauto_venv` and activate it.
2. Use `python -m pip list` to check installed packages.
3. Start `IPython` (`python -m IPython`).
4. Inside IPython, create three variables following PEP 8 `snake_case` rules:
   - `router_hostname` assigned to `"br-spo-core-01"`
   - `bgp_asn` assigned to `65100`
   - `ospf_area` assigned to `"0.0.0.0"`
5. Use `type()` on each variable to verify whether Python sees it as a string (`str`) or an integer (`int`).

### Exercise 2: Interactive Device Inventory Script
Create a file named `device_prompt.py` that performs the following actions:
1. Includes the proper Linux shebang line at the top.
2. Uses `input()` to ask the user for a **Device Hostname**.
3. Uses `input()` to ask the user for a **Management IP Address**.
4. Prints a clean summary to standard output using `print()`.

**Example Solution (`device_prompt.py`):**
```python
#!/usr/bin/env python

# Prompt the network engineer for device details
device_hostname = input("Enter the device hostname: ")
mgmt_ip_addr = input("Enter the management IP address: ")

# Print the collected information to standard output
print("----------------------------------------")
print("Target Device Hostname:", device_hostname)
print("Target Management IP:  ", mgmt_ip_addr)
print("Data type of IP var:   ", type(mgmt_ip_addr))
print("----------------------------------------")
```

### Exercise 3: Spot the Syntax & PEP 8 Errors
Look at the broken code snippet below. As a network automation engineer, identify **4 things** that are either invalid Python syntax or violate PEP 8 conventions:

```python
1st_router = "10.0.0.1"
core-switch-ip = "10.0.0.2"
MyRouterName = "edge-rtr-01"
__custom_vlan__ = 100
```

**Answers:**
1. `1st_router`: **Syntax Error!** Variable names cannot start with a number (`1`). Fix: `first_router` or `router_1`.
2. `core-switch-ip`: **Syntax Error!** Hyphens (`-`) are not allowed in variable names because Python treats them as the minus sign. Fix: `core_switch_ip`.
3. `MyRouterName`: **PEP 8 Violation!** Mixed capitalization (`PascalCase`) is reserved for Classes. Regular variables should use `snake_case`. Fix: `my_router_name`.
4. `__custom_vlan__`: **Convention Violation!** Double leading and trailing underscores (*dunder*) are reserved for Python's internal magic variables. Fix: `custom_vlan`.

---

## 9. Quick Reference Cheat Sheet (Week 1)

| Task / Concept | Command / Syntax | Notes for Network Engineers |
| :--- | :--- | :--- |
| **Create Virtual Env (Linux/Mac)** | `python3 -m venv <name>` | Isolates packages like a VRF. |
| **Activate Virtual Env (Linux/Mac)** | `source <name>/bin/activate` | Must be active before running scripts. |
| **Create Virtual Env (Windows)** | `py -m venv <name>` | Uses the Windows `py` launcher. |
| **Activate Virtual Env (Windows)** | `<name>\Scripts\activate` | Changes command prompt to `(<name>)`. |
| **List Installed Packages** | `python -m pip list` | Safer than running `pip list` alone. |
| **Install Requirements File** | `python -m pip install -r requirements.txt` | Installs all course dependencies at once. |
| **Start Interactive Shell** | `python -m IPython` | Great for testing code snippets live. |
| **Assign a Variable** | `my_ip = "10.1.1.1"` | Single `=` assigns right value to left name. |
| **Print Output (`stdout`)** | `print(my_ip)` | Displays value on the terminal screen. |
| **Read User Input (`stdin`)** | `val = input("Prompt: ")` | Always returns a string (`str`). |
| **Check Data Type** | `type(val)` | Returns `<class 'str'>`, `<class 'int'>`, etc. |
| **Linux Shebang Line** | `#!/usr/bin/env python` | First line of `.py` file; finds active `venv`. |
| **Make Script Executable (Linux)** | `chmod +x script.py` | Allows running `./script.py` directly. |
