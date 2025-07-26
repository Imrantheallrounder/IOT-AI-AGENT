#!/usr/bin/env python3
"""
Example usage of the device management functions.
"""

from loader import (
    add_device, update_device, get_all_devices, delete_device, 
    find_device_by_id, load_devices_from_yaml
)


def example_usage():
    """Demonstrate the device management functions."""
    filepath = "devices/devices.yaml"
    
    print("=== IoT Device Management Example ===\n")
    
    # 1. List all current devices
    print("1. Current devices:")
    devices = get_all_devices(filepath)
    for device in devices:
        print(f"   - {device.device_id}: {device.device_name} ({device.device_location})")
    print()
    
    # 2. Add a new device
    print("2. Adding a new device...")
    try:
        new_device = add_device(
            device_id="ac-003",
            device_name="air conditioner",
            device_description="Central air conditioning unit",
            device_location="master_bedroom",
            device_type="ac",
            mqtt_topic="master_bedroom",
            capabilities=["on_off", "temperature", "fan_speed"],
            filepath=filepath
        )
        print(f"   ✓ Added device: {new_device.device_id}")
    except ValueError as e:
        print(f"   ⚠ {e}")
    print()
    
    # 3. Get a specific device
    print("3. Getting device details...")
    registry = load_devices_from_yaml(filepath)
    device = find_device_by_id(registry, "bulb-001")
    if device:
        print(f"   Device: {device.device_id}")
        print(f"   Name: {device.device_name}")
        print(f"   Location: {device.device_location}")
        print(f"   Capabilities: {', '.join(device.capabilities)}")
    print()
    
    # 4. Update a device
    print("4. Updating device...")
    try:
        updated_device = update_device(
            "bulb-001", 
            filepath,
            device_description="Smart LED bulb with dimming capability",
            capabilities=["on_off", "brightness", "color"]
        )
        print(f"   ✓ Updated device: {updated_device.device_id}")
        print(f"   New capabilities: {', '.join(updated_device.capabilities)}")
    except ValueError as e:
        print(f"   ⚠ {e}")
    print()
    
    # 5. List devices again to see changes
    print("5. Updated device list:")
    devices = get_all_devices(filepath)
    for device in devices:
        print(f"   - {device.device_id}: {device.device_name} ({device.device_location})")
        print(f"     Capabilities: {', '.join(device.capabilities)}")
    print()
    
    # 6. Delete a device (commented out to avoid data loss)
    print("6. To delete a device, uncomment the following code:")
    print("   # delete_device('ac-003', filepath)")
    print("   # print('   ✓ Deleted device: ac-003')")
    print()


if __name__ == "__main__":
    example_usage() 