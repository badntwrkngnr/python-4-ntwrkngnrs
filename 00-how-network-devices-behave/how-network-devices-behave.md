# Module 00: How Network Devices Behave

## Overview

As network engineers, we spend years mastering the Command Line Interface (CLI) of routers, switches, and firewalls. However, managing dozens or hundreds of devices box-by-box does not scale.

When you introduce **Python** into your workflow, your perspective changes: instead of treating each router as an isolated box, you start **treating the network as an integrated, programmable system**.

---

## Key Concepts Covered in This Module

### 1. The Networking Analogy: Virtual Environments (`venv`) are like

* **The Problem:** Your operating system uses a "system Python" for internal tools. If you install automation libraries globally, version conflicts can break your environment.
* **The Solution:** A Python Virtual Environment (`venv`) is an **isolated sandbox**—exactly like a **VRF (Virtual Routing and Forwarding)** or a VLAN. It isolates your project dependencies without affecting the host operating system.

### 2. The Interactive Shell (IPython REPL)

* **The Analogy:** Using **IPython** for testing code snippets is just like typing `show ip interface brief` directly into a router's CLI to inspect live states.
* **Script Files (`.py`):** Writing a Python script file is like preparing a full configuration template and pushing it to the device.

---

## Quick Setup & Lab Execution

1. Create and activate your virtual environment:

   ```bash
   python3 -m venv netauto_venv
   source netauto_venv/bin/activate
   ```
