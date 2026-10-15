import json
from datetime import datetime
from pathlib import Path

import ip_router

# Resolve data files next to this script, so it works from any directory
HERE = Path(__file__).resolve().parent

border_router = ip_router.Router("border-router-1")

with open(HERE / "test_routing_table.json") as f:
    border_router.RIB = json.load(f)
    border_router.calculate_fib()

with open(HERE / "test_destinations.txt") as f:
    # splitlines() + filter: a trailing newline must not become an empty "IP"
    destinations = [line.strip() for line in f.read().splitlines() if line.strip()]

t1 = datetime.now()

for destination in destinations:
    border_router.incoming_packet(destination)

t2 = datetime.now()

duration = t2 - t1
number_of_packets = len(destinations)
duration_per_packet = duration.total_seconds() / number_of_packets
packets_per_second = 1 / duration_per_packet
print(f"{border_router.hostname} packets per second: {int(packets_per_second)}")
