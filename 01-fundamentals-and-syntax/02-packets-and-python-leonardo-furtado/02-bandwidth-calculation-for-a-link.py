interface_speed_mbps = 100
channel_count = 4

total_bandwidth = interface_speed_mbps * channel_count

print("Each channel supports: " + str(interface_speed_mbps) + " Mbps")
print("Number of channels: " + str(channel_count))
print("Total link bandwidth: " + str(total_bandwidth) + " Mbps")