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
        self.devices = [d for d in self.devices if d.hostname != hostname]

    def list_devices(self):
        if not self.devices:
            print("No devices in inventory.")
        else:
            for device in self.devices:
                print(device.get_summary())

    def update_device_status(self, hostname, new_status):
        for device in self.devices:
            if device.hostname == hostname:
                device.update_status(new_status)
                return True
        return False


def main():
    inventory = InventoryManager()  # must be created before the loop

    while True:
        print("\nNetwork Inventory Management")
        print("1. Add Device")
        print("2. Remove Device")
        print("3. List Devices")
        print("4. Update Device Status")
        print("5. Exit")

        choice = input("Choose an option: ")

        match choice:
            case '1':
                hostname = input("Hostname: ")
                device_type = input("Device Type (router/switch/firewall): ")
                ip_address = input("IP Address: ")
                status = input("Status (up/down/maintenance): ")
                inventory.add_device(NetworkDevice(hostname, device_type, ip_address, status))
                print(f"✅ Device '{hostname}' added.")

            case '2':
                hostname = input("Enter hostname to remove: ")
                inventory.remove_device(hostname)
                print(f"🗑️ Device '{hostname}' removed (if it existed).")

            case '3':
                print("\n📋 Device List:")
                inventory.list_devices()

            case '4':
                hostname = input("Hostname to update: ")
                new_status = input("New status (up/down/maintenance): ")
                if inventory.update_device_status(hostname, new_status):
                    print(f"🔄 Status of '{hostname}' updated.")
                else:
                    print("⚠️ Device not found.")

            case '5':
                print("👋 Exiting inventory system. Goodbye!")
                break

            case _:
                print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()