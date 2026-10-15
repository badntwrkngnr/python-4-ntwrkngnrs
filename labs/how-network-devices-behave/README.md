# Lab: How Network Devices Behave

As network engineers we spend years on the CLI of routers and switches. Writing the *behaviour* of those devices in Python is a good way to learn both at the same time: each script is a tiny, runnable model of a real device.

> **Source:** origin of these scripts is not documented yet. Add the author/course link here before sharing the repository widely.

## Scripts

| # | Script | What it models | Python concepts used |
| :-: | :--- | :--- | :--- |
| 01 | [`ethernet_hub.py`](01-ethernet-hub/ethernet_hub.py) | A hub: a signal received on one port is repeated on **every other** port | `list`, `while True`, `input()`, `int()`, `if`/`else`, `for`, `try`/`except` |
| 02 | [`arp_cache.py`](02-arp-cache/arp_cache.py) | An ARP table lookup (`show ip arp`), with an *Incomplete* entry on a miss | `dict`, `.get()`, truthiness, f-strings, `.items()` |
| 03 | [`ethernet_switch.py`](03-ethernet-switch/ethernet_switch.py) | A switch: MAC learning, known-unicast forwarding, flooding for unknown/broadcast, interface counters (`show mac address-table`, `show interfaces`) | nested `dict`, functions, `+=`, `sorted()`, string slicing |
| 04 | [`ip_router.py`](04-ip-router/ip_router.py) | A router: RIB → FIB, **longest prefix match**, forward or drop (`show ip route`) | classes, `ipaddress`, `json`, `try`/`except` |

Suggested order: 01 → 02 → 03 → 04. Each step adds one idea (flooding → address resolution → learning → routing).

## How to run

Activate your virtual environment first (see the [Week 1 guide](../../01-fundamentals-and-syntax/guide.md)), then:

```bash
cd labs/how-network-devices-behave

python 01-ethernet-hub/ethernet_hub.py        # type a port number 0-3; anything else exits
python 02-arp-cache/arp_cache.py              # try 172.16.0.31, then an unknown IP
python 03-ethernet-switch/ethernet_switch.py  # replays 28 frames and prints both tables
python 04-ip-router/ip_router.py              # type an IPv4 address; 'quit' exits
```

### Router benchmark (`test_router.py`)

`test_router.py` loads 100 routes from `test_routing_table.json`, sends the 80 addresses in `test_destinations.txt` through the router and prints the packets-per-second rate. About a quarter of the destinations have no matching route, so you will see both *Forwarding* and *Dropping* in the output.

```bash
python 04-ip-router/test_router.py
```

The result depends on your machine, and printing every decision slows the router down. That is a good starting point for a discussion about why a real FIB is not a Python list scanned from start to finish.

## Things worth noticing while you read the code

- **Switch vs. hub:** the switch learns the *source* MAC on every frame and floods only when the destination is unknown or broadcast.
- **RIB vs. FIB:** `add_route()` rebuilds the whole FIB every time. Fine for a lab, not for 900k BGP routes.
- **Longest prefix match** in `find_next_hop_address()` is a linear scan that keeps the candidate with the largest `prefixlen`.
- **Instance state:** `RIB` and `FIB` live on the instance (`self.RIB`). If they were class attributes, every `Router` would share the same lists, which is the mutable-aliasing trap from the [Week 2 guide](../../02-data-types-files-and-lists/guide.md).
