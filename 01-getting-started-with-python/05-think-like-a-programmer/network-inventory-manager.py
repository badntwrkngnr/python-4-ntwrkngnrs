class NetworkDevice:
    def __init__(self, hostname, device_type, ip_address, status):
        self.hostname = hostname
        self.device_type = device_type
        self.ip_address = ip_address
        self.status = status

    def get_summary(self):
        return f"Hostname: {self.hostname}, Type: {self.device_type}, IP: {self.ip_address}, Status: {self.status}"

    def update_status(self, new_status):
        self.status = new_status


class InventoryManager:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def remove_device(self, hostname):
        self.devices = [device for device in self.devices if device.hostname != hostname]

    def list_devices(self):
        if not self.devices:
            print("No devices in inventory.")
        else:
            for device in self.devices:
                print(device.get_summary())


# Main Program
inventory = InventoryManager()

while True:
    print("\nNetwork Inventory Management")
    print("1. Add Device")
    print("2. Remove Device")
    print("3. List Devices")
    print("4. Update Device Status")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        hostname = input("Hostname: ")
        device_type = input("Device Type (router/switch/firewall): ")
        ip_address = input("IP Address: ")
        status = input("Status (up/down/maintenance): ")
        device = NetworkDevice(hostname, device_type, ip_address, status)
        inventory.add_device(device)
        print(f"✅ Device '{hostname}' added.")

    elif choice == '2':
        hostname = input("Enter hostname to remove: ")
        inventory.remove_device(hostname)
        print(f"🗑️ Device '{hostname}' removed (if it existed).")

    elif choice == '3':
        print("\n📋 Device List:")
        inventory.list_devices()

    elif choice == '4':
        hostname = input("Hostname to update: ")
        new_status = input("New status (up/down/maintenance): ")
        for device in inventory.devices:
            if device.hostname == hostname:
                device.update_status(new_status)
                print(f"🔄 Status of '{hostname}' updated.")
                break
        else:
            print("⚠️ Device not found.")

    elif choice == '5':
        print("👋 Exiting inventory system. Goodbye!")
        break

    else:
        print("❌ Invalid option. Please try again.")
