hostname = "PE1"
device_model = "Cisco ASR 9001"
boot_year = 2015
current_year = 2025
uptime_years = current_year - boot_year

print("Device " + hostname + " (" + device_model + ") has been up for " + str(uptime_years) + " years.")