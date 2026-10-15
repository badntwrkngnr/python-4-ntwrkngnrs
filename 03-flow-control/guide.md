---
title: "Week 3 — Flow Control"
source: "Study notes based on Kirk Byers, Learning Python for Network Engineers (Lesson 3)"
status: needs-review
---

# Learning Python for Network Engineers — Week 3 Study Guide (Lesson 3)
**Course Reference:** Kirk Byers (*Learning Python for Network Engineers* / Lesson 3)  
**Target Audience:** Network engineers moving into network automation  
**Language Level:** English (B1/B2 Intermediate)

---

## 1. Introduction: Flow Control and the Network as a System

In Weeks 1 and 2, you learned how to isolate virtual environments (`venv`), follow the PEP 8 style guide, and work with variables, numbers (`int` and `float`), booleans (`bool`), the `None` type, files with context managers (`with`), lists (`list`), and tuples (`tuple`). When you learn Python, you stop configuring routers and switches one by one ("box by box"). Instead, you start to **treat the network as one integrated system**.

In **Lesson 3**, we move on to flow control in network automation:
* **Conditionals (`if` / `elif` / `else`):** Let your code make logical decisions based on the state of the network.
* **Loops (`for` and `while`):** Let you go through collections of devices or wait for operational events, using controls such as `break` and `continue`.
* **List Comprehensions:** A short and dynamic way to create a new list from an existing one (optional / intermediate content).
* **Generator Expressions:** Very similar to list comprehensions. They let you create generators on the fly and use them in later `for` loops without using up your RAM (optional / intermediate content).

---

## 2. Conditionals in Python

Conditional statements are the basis of decision-making in Python.

### Basic `if` Syntax
A conditional starts with the keyword `if`, followed by an expression that evaluates to a boolean `True` or `False`. The line ends with a colon (`:`). The colon marks the start of an indented block of code (use 4 spaces, as PEP 8 recommends). This block runs only if the expression evaluates to `True`.

```python
# Checking if the subnet '10.1' exists inside an IP address string
ip_addr = "10.1.20.5"

if "10.1" in ip_addr:
    print("Found address")
```
In the example above, we check whether the substring `"10.1"` is contained (`in`) in the larger string. The expression is `True`, so the message in the indented block is printed.

---

### Multiple Choices: `elif` and `else`
When we need to check more than one possibility, we combine `if` with the `elif` (*else if*) and `else` clauses:
* **`if`:** This is the only required part of a conditional. If its expression is `True`, its block runs.
* **`elif`:** This is optional. It is checked only if the previous condition (the `if` or an earlier `elif`) was `False`. You can have many `elif` blocks (1, 5, or 10) in a row.
* **`else`:** This is optional and works as a catch-all. It runs only if **all** the previous `if` and `elif` conditions were `False`.
* **Mutual Exclusion:** Only **one block** in the whole `if` / `elif` / `else` chain will run.

---

### Comparison Operators
To build conditional expressions, we use comparison operators:
* `==` : Equal to (compares values; this is different from the single `=`, which assigns a value to a variable).
* `!=` : Not equal to.
* `>` and `>=` : Greater than / Greater than or equal to.
* `<` and `<=` : Less than / Less than or equal to.

```python
ssh_timeout = 20

if ssh_timeout == 10:
    print("SSH timeout is equal to 10")
elif ssh_timeout > 30:
    print("SSH timeout is greater than 30")
else:
    print("SSH timeout is between 10 and 30 (and not 10)")
```
In this example, Python checks whether `ssh_timeout` is equal to `10` (false). Then it checks in the `elif` whether it is greater than `30` (false). Finally, it runs the `else` block.

---

### Logical Operators (`and`, `or`, `not`)
You can combine several expressions using boolean logic:
* **`and`:** Both expressions must be `True` for the whole result to be `True`.
* **`or`:** At least one of the expressions must be `True` for the block to run.
* **`not`:** Reverses the boolean value of the expression (`True` becomes `False`, and `False` becomes `True`).

```python
ssh_timeout = 10
host_reachable = True
ip_addr = "10.1.1.1"

if host_reachable and ssh_timeout >= 10:
    print("Try to connect")
elif not host_reachable or ip_addr == "10.1.1.1":
    print("Host unreachable or matched specific IP")
else:
    print("Default fallback action")
```
In the code above, `host_reachable` is `True` and `ssh_timeout >= 10` is also `True`, so the `and` condition is met and the script prints `"Try to connect"`. If one of them were `False`, Python would go on to the `elif` and check `not host_reachable` or the IP address match.

---

### Nesting Conditionals
You can put conditionals inside other conditionals, at many levels of depth. Each new block that starts with a colon (`:`) adds 4 more spaces of indentation:

```python
host_reachable = True
ssh_timeout = 10

if host_reachable:
    if ssh_timeout is not None:
        print("Try to connect")
```
If `host_reachable` is `True`, we enter the first indented block and check the second conditional (`if ssh_timeout is not None:`).

---

### Idiomatic Expressions
Python has preferred (idiomatic) ways to write certain checks. They make your code easier to read and help you avoid warnings from code analysis tools (*linters*):
* When you compare a variable with `None`, `True`, or `False`, use the identity operator **`is`** or **`is not`** instead of `==`.
* There is only one `None` object in Python's memory, so the correct way is `if ssh_timeout is None:` or `if ssh_timeout is not None:` (instead of `ssh_timeout == None` or `not ssh_timeout is None`).
* In the same way, linters prefer `if host_unreachable is False:` or `if host_unreachable is True:` when you compare directly with booleans.

---

### Reminder About "Truthy" and "Falsy" Values and Type Traps
As you saw in Week 2 and again in Lesson 3, each data type in Python has **exactly one value that evaluates to `False`** in a boolean context. Any other value of that type evaluates to `True`:
* **Integers (`int`):** The `False` value is `0` (any other integer is `True`).
* **Strings (`str`):** The `False` value is the empty string `""`.
* **Lists (`list`):** The `False` value is the empty list `[]`.
* **Floats (`float`):** The `False` value is `0.0`.
* **`NoneType`:** The value `None` also evaluates to `False`.

> **Be careful in network automation:**
> If you write `if not ssh_timeout:`, the condition is `True` **both** when `ssh_timeout` is `0` and when it is `None`. If your script needs to treat a timeout of zero (`0`) differently from an undefined timeout (`None`), you must check the identity explicitly (for example, `if ssh_timeout is None:`) to get exactly the behavior you want.

---

## 3. `for` Loops

The `for` loop is one of the most basic ways to repeat actions in Python. It is designed to go through a collection of items.

### Syntax and Iterators
The syntax uses the keyword `for`, followed by a **loop variable**, the keyword `in`, the **iterator** (the collection of items to go through), a colon (`:`), and the indented block of code:

```python
ip_list = ["10.88.17.1", "10.88.17.2", "10.88.17.20"]

for ip in ip_list:
    print(ip)
```
* On each pass through the `for` loop, the variable `ip` receives one element of the list in order (`"10.88.17.1"` on the first pass, `"10.88.17.2"` on the second, `"10.88.17.20"` on the third). The original list stays unchanged.
* **What is an iterator?** It is any collection or object in Python that gives you one element at a time when you go through it in a loop. This includes lists (`list`), tuples (`tuple`), dictionaries (`dict`), strings (`str`), and `range` objects.
* **Looping through strings:** If you write `for letter in some_string:`, the iterator returns one character at a time on each repetition.
* **Important rule:** Never change the collection (adding or removing items) while you are looping through it in a `for` loop.

---

### Controlling the Loop: `break` and `continue`

1. **`break` (immediate exit):** Stops the `for` loop and exits it right away.
   ```python
   for i in range(10):
       print(i)
       if i == 5:
           break
   ```
   In this example, `range(10)` generates the numbers from `0` to `9`. But when `i` reaches `5`, it prints `5`, enters the `if i == 5:` condition, and runs `break`, which ends the loop immediately.

2. **`continue` (skip to the next iteration):** Does not end the loop. Instead, it stops the current iteration and jumps straight back to the top of the `for` loop to process the next element.
   ```python
   for i in range(10):
       if i == 5:
           continue
       print(i)
   ```
   Here, when `i == 5`, `continue` makes Python skip the `print(i)` command and go back to the top of the loop to continue with the number `6`.

---

### Nested Loops and Tuple Unpacking
You can put a `for` loop inside another `for` loop, at many levels of depth. Also, if the outer structure is a list of tuples, Python automatically does **unpacking** in the `for` statement:

```python
data_centers = [
    ("sf1", "10.1.1"),
    ("sf2", "10.1.2")
]

for dc, base_addr in data_centers:
    for net_addr in range(1, 5):
        print(dc, base_addr + "." + str(net_addr))
```
* On the first pass of the outer loop, the first tuple is automatically unpacked into `dc = "sf1"` and `base_addr = "10.1.1"`.
* Then the inner loop goes through `range(1, 5)` (which generates `1, 2, 3, 4`) and prints the addresses `10.1.1.1` to `10.1.1.4`.
* When the inner loop finishes number `4`, Python goes back to the outer loop, moves to `"sf2"` and `"10.1.2"`, and repeats the whole inner loop.

---

### Getting the Index and the Value with `enumerate()`
Instead of using the `range(len(some_list))` pattern, the idiomatic and recommended way in Python to get both the **index** and the **value** of a collection is the built-in function **`enumerate()`**:

```python
data_centers = ["sf1", "sf2", "la1", "la2", "dallas"]

for i, dc in enumerate(data_centers):
    print(i, dc)
```
The `enumerate()` function returns a tuple with two elements `(index, value)` on each pass through the loop. On the first iteration, `i = 0` and `dc = "sf1"`. On the second, `i = 1` and `dc = "sf2"`, and so on.

---

### Special Cases: Empty List, `pass`, and the `else` Clause in `for`
* **Looping through an empty list (`[]`):** If you run `for element in empty_list:`, there is no syntax error. Python simply sees that there are no elements and leaves the loop right away without running the inner block.
* **The `pass` keyword (no-op):** It works as a null operation (*no-op*) or placeholder. Use it when the syntax needs an indented block but you do not want to take any action yet:
  ```python
  for dc in data_centers:
      pass
  ```
* **The `else` clause in a `for` loop:** `for` loops have an optional `else` clause. It runs at the end of the loop **only if the loop never hit a `break`**:
  ```python
  # Example 1: The break happens at 5, so the else block does NOT run
  for i in range(10):
      if i == 5:
          break
  else:
      print("Loop completed without break")

  # Example 2: range(10) goes from 0 to 9 (it never reaches 12), so the break never happens and the else DOES run
  for i in range(10):
      if i == 12:
          break
  else:
      print("Never hit break - executing else block!")
  ```

---

## 4. `while` Loops

The `while` loop is another way to repeat actions in Python. Its execution depends on a boolean condition.

### Syntax and Exit Condition
The syntax is the keyword `while`, followed by an expression that evaluates to `True` or `False`, and a colon (`:`). While the expression is `True`, Python runs all the statements in the indented block, goes back to the top of the `while`, and checks the expression again.

To exit a `while` loop, **something must happen** inside the loop:
1. The expression at the top of the `while` evaluates to `False`; **or**
2. The execution reaches a `break` statement.

```python
i = 1
while i <= 5:
    print(i)
    i += 1
```

---

### The Danger of Infinite Loops
When you work with `while`, you must be very careful not to create an **infinite loop** by accident, especially when you use the `continue` statement:

```python
# WARNING: Example of an infinite loop!
i = 0
while i <= 5:
    if i == 3:
        continue  # Jumps back to the top WITHOUT increasing the variable 'i'!
    print(i)
    i += 1
```
In the faulty code above, the program prints `0`, `1`, and `2`. But when `i` becomes `3`, it enters `if i == 3:` and runs `continue`. This sends it straight back to the top of the `while` without ever reaching the `i += 1` line. As a result, the variable `i` stays stuck at `3` forever (`3 <= 5` is always `True`). To fix this, you must increase the variable (`i += 1`) **before** the `continue` statement.

---

### Similarities with `for`, the `while True` Pattern, and Nesting
* **Similarities with the `for` loop:** Like `for`, the `while` loop supports `break`, `continue`, and the optional `else` clause (which runs only if no `break` happens inside the `while` loop).
* **The `while True:` pattern:** It is very common to see the literal `True` in the top expression (`while True:`). The literal `True` will never become `False`, so the only way out of this loop is to reach an inner `break` statement (for example, when a timeout is reached or a router sends a response).
* **Nesting loops:** You can put a `while` loop inside another `while` loop, or a `for` loop inside a `while` loop, at many levels of depth.

### When to Use `for` and When to Use `while`

| Structure | Mental Model | Use in Network Automation |
| :--- | :--- | :--- |
| **`for` loop** | **"For each":** Goes through a defined collection of elements until it is finished. | Going through a list of IP addresses, the lines of a `show` command output file, or the ports of a switch. |
| **`while` loop** | **Event-based:** Stays in the loop until a specific event happens. | Waiting for a BGP session to come up, watching a 5-second timeout, or testing SSH connectivity again and again. |

---

## 5. List Comprehensions (*Optional / Intermediate*)

*Note: As Kirk Byers points out, both list comprehensions and generator expressions are intermediate, optional topics. If they seem confusing at first, you can skip them and come back later.*

### Why Do List Comprehensions Exist, and How Do You Read Them?
List comprehensions give you a short and dynamic way to create a **new list** from an existing iterator, without changing the original list.

The syntax is wrapped in square brackets `[]` and looks "backwards" at first. **Kirk Byers' reading tip:**
1. First, find the `for` loop inside the brackets (for example, `for x in my_list`).
2. Then look at the expression at the **start** of the brackets (`x ** 2`). It defines what goes into the new list on each iteration.

```python
my_list = [0, 1, 2, 3, 4]

# Creates a new list with the squares (x ** 2) of each element in my_list
new_list = [x ** 2 for x in my_list]
print(new_list)  # Result: [0, 1, 4, 9, 16]
```

---

### Adding Conditionals (`if`) to List Comprehensions
We can add an `if` condition at the end of the list comprehension to filter which elements go into the new list:

```python
# Keeps only the even numbers (where the remainder of the division by 2 is zero: x % 2 == 0)
even_numbers = [x for x in range(10) if x % 2 == 0]
print(even_numbers)  # Result: [0, 2, 4, 6, 8]
```
Here, Python goes through `0` to `9` (`range(10)`), checks in the condition whether `x % 2 == 0` (an even number), and adds `x` to the new list only if the condition is true.

---

### Multiple `for` Loops in List Comprehensions
You can also use several `for` loops inside one list comprehension (and even split it across several indented lines to make it easier to read):

```python
# Generating IP addresses dynamically with two for loops and one condition
ip_list = [
    "172.16." + str(x) + "." + str(y)
    for x in range(10)
    for y in range(3)
    if x == 9
]
print(ip_list)
# Result: ['172.16.9.0', '172.16.9.1', '172.16.9.2']
```
* The first loop (`for x in range(10)`) works as the outer loop (`0` to `9`).
* For each value of `x`, the second loop (`for y in range(3)`) goes through `0, 1, 2`.
* The condition `if x == 9` keeps only the cases where `x` equals `9`, which gives the final list `['172.16.9.0', '172.16.9.1', '172.16.9.2']`.

---

## 6. Generator Expressions (*Optional / Intermediate*)

### The Memory Problem with Huge Lists
When you create a list in Python (with `list()` or with a list comprehension), Python stores **all the elements in RAM at the same time**.
* If you run `list(range(10000000))` (10 million elements) in IPython, you can already see a delay in the response time.
* If you try `list(range(100000000))` (100 million elements), Python refuses the operation and raises a memory error (`MemoryError`).

### What Is a Generator and a Generator Expression?
Instead of reserving memory for all 100 million items at once, a **generator** starts the process, returns only the first element, **remembers its current state**, and uses an algorithm to calculate and return the next value only when it is asked for.
* Traditional generator functions use the `yield` statement to return values one after another.
* A **Generator Expression** is a syntax shortcut for creating a generator on the fly, without writing a full function with `yield`.

### Syntax: Parentheses `()` Instead of Square Brackets `[]`
The syntax of a generator expression is the same as a list comprehension, except that you use **parentheses `()`** instead of square brackets `[]`:

```python
# Creates a generator expression (it does not store all the elements in memory!)
my_gen = (x ** 2 for x in range(10))

# Using the elements on demand inside a for loop
for val in my_gen:
    print(val)
```
As with list comprehensions, you can use several `for` loops and `if` statements inside a generator expression to create IP addresses on demand, even for ranges of 100 million items.

### The Big Gotcha with Generators: One-Time Use!
A generator only keeps its current state to calculate the next item, so **once you go through all the elements of a generator, it is exhausted**:
* Unlike a list (where you can run a second `for` loop and Python automatically starts again from index `0`), if you try to use the same exhausted generator in a second `for` loop, **nothing will be returned**.
* To go through the data again, you must **re-create** the generator expression.

---

## 7. Hands-On Practice: Week 3 Exercises (Lesson 3 Exercises)

Below are explanations and commented solutions for the 5 practice exercises from Lesson 3. They use the concepts from Weeks 1, 2, and 3.

### Exercise 1: Subnet Calculator with a Loop
**Goal:** Define the base address `"192.168.254."`. Ask the user (`input()`) for a subnet prefix between `25` and `30` (convert it to an integer). Calculate the subnet size ($2^{\text{host bits}}$), the number of usable hosts ($\text{size} - 2$), and the total number of subnets. Then use a `for` loop to print all the subnet network addresses, plus the first and last host of the first subnet.

```python
#!/usr/bin/env python

base_addr = "192.168.254."
prefix_len = int(input("Enter a subnet prefix length (25-30): "))

# Calculate host bits, subnet size, usable hosts, and total number of subnets
host_bits = 32 - prefix_len
subnet_size = 2 ** host_bits
num_hosts = subnet_size - 2
num_subnets = 256 // subnet_size

print("Subnets:")
print(" Number of subnets:", num_subnets)

# for loop to print each subnet number
for i in range(num_subnets):
    subnet_octet = i * subnet_size
    print(" Subnet Number:", base_addr + str(subnet_octet))

print("Number of hosts per subnet:", num_hosts)
print("First host in first subnet:", base_addr + "1")
print("Last host in first subnet: ", base_addr + str(subnet_size - 2))
```

---

### Exercise 2: Find an Interface and IP (`10.220.x.x`) in a CLI File
**Goal:** Read the file `show_ip_int_brief.txt` using a context manager (`with`). Go through its lines with a `for` loop. Find the line that belongs to the `"10.220"` network using a simple string check (`in`), and extract the interface name (`intf_name`) and the IP address (`ip_addr`).

```python
#!/usr/bin/env python

with open("show_ip_int_brief.txt", mode="r") as f:
    for line in f:
        if "10.220" in line:
            fields = line.split()
            intf_name = fields[0]
            ip_addr = fields[1]
            print("Interface:", intf_name)
            print("IP Address:", ip_addr)
```

---

### Exercise 3: Timeout Monitoring with a `while` Loop
**Goal:** Create a program that stays in a `while` loop until a `5`-second timeout expires. Use `import time`, `start_time = time.time()`, and `time.sleep(1)` inside the loop. Print the elapsed time on each pass and the total time when you leave the loop.

```python
#!/usr/bin/env python
import time

timeout = 5
start_time = time.time()

while (time.time() - start_time) < timeout:
    time.sleep(1)
    elapsed = time.time() - start_time
    print("Elapsed time inside loop:", round(elapsed, 2), "seconds")

total_elapsed = time.time() - start_time
print("Exited while loop! Total elapsed time:", round(total_elapsed, 2), "seconds")
```

---

### Exercise 4: Creating Matching Lists of Interfaces and IP Addresses
**Goal:** Read the file `show_ip_int_brief.txt`, go through its content, and find all the interfaces that have an IP address assigned (assume they start with `"10."`). Save the interface names and the IP addresses in two lists with the same order, and print them.

```python
#!/usr/bin/env python

interfaces = []
ip_addresses = []

with open("show_ip_int_brief.txt", mode="r") as f:
    for line in f:
        if "10." in line:
            fields = line.split()
            interfaces.append(fields[0])
            ip_addresses.append(fields[1])

print("Interfaces:", interfaces)
print("IP Addresses:", ip_addresses)
```

---

### Exercise 5: Processing a Junos ARP Table (`junos_show_arp.txt`)
**Goal:** Read the file `junos_show_arp.txt`, extract the mappings from IP address to MAC address, and change the MAC address format from `'06:1a:97:b0:c4:89'` to `'06-1a-97-b0-c4-89'`. Print the pairs to standard output.

```python
#!/usr/bin/env python

with open("junos_show_arp.txt", mode="r") as f:
    for line in f:
        # Skip header or summary lines by checking for a MAC address with ':'
        if ":" in line:
            fields = line.split()
            mac_addr = fields[0].replace(":", "-")
            ip_addr = fields[1]
            print(ip_addr, "-->", mac_addr)
```

---

## 8. Quick Reference Cheat Sheet — Week 3

| Category | Concept / Operation | Python Syntax | Behavior for Network Engineers |
| :--- | :--- | :--- | :--- |
| **Conditionals** | `if` / `elif` / `else` decision | `if expr:` / `elif expr:` / `else:` | Runs only **one** block (the first one whose condition is `True`). |
| **Conditionals** | Value comparison | `==`, `!=`, `>`, `>=`, `<`, `<=` | Checks equality, difference, or size and returns `True` or `False`. |
| **Conditionals** | Idiomatic expressions | `is None` / `is not None` | Preferred by linters over `== None` or `!= None`. |
| **Conditionals** | "Falsy" values (`False`) | `0`, `0.0`, `""`, `[]`, `None` | Any other number, or any non-empty string or list, evaluates to `True`. |
| **`for` loop** | Iterating over a collection | `for ip in ip_list:` | Goes through each element of an iterator (list, tuple, string, file). |
| **`for` loop** | Index + value | `for i, val in enumerate(lst):` | Returns an `(index, element)` tuple on each iteration. |
| **`for` loop** | Unpacking | `for dc, ip in dc_tuples:` | Automatically unpacks tuples from a list into several variables. |
| **Control** | Exit the loop (`break`) | `break` | Stops and exits the `for` or `while` loop immediately. |
| **Control** | Skip an iteration (`continue`) | `continue` | Skips the rest of the current block and goes back to the top of the loop. |
| **Control** | Null operation (`pass`) | `pass` | Placeholder (*no-op*) when the block should do nothing. |
| **Control** | `else` clause in loops | `for ...: ... else:` | The `else` block runs only if the loop ends **without** hitting a `break`. |
| **`while` loop** | Event-based repetition | `while expression:` | Stays in the loop while the expression is `True`. |
| **`while` loop** | Loop that exits with `break` | `while True:` | Runs forever until it reaches an inner `break` statement. |
| **Advanced** | List comprehension | `[x**2 for x in lst if x > 0]` | Creates a new list in memory on the fly, using square brackets `[]`. |
| **Advanced** | Generator expression | `(x**2 for x in range(1000000))` | Uses parentheses `()`. It creates items on demand without filling the RAM, and it is exhausted after the first full use. |
