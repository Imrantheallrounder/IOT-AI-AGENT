import yaml
from pathlib import Path
from .models import DeviceRegistry, Device


def load_devices_from_yaml(filepath: str = "devices/devices.yaml") -> DeviceRegistry:
    """Load and validate device registry from YAML file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"{filepath} not found")
    
    with path.open("r") as f:
        raw = yaml.safe_load(f)
    
    return DeviceRegistry(**raw)


def get_all_devices(filepath: str = "devices.yaml"):
    """Get all devices from the registry."""
    try:
        registry = load_devices_from_yaml(filepath)
        return registry.devices
    except FileNotFoundError:
        return []


def save_devices_to_yaml(registry: DeviceRegistry, filepath: str = "devices.yaml"):
    """Save device registry to YAML file."""
    path = Path(filepath)
    with path.open("w") as f:
        yaml.dump(registry.model_dump(), f, default_flow_style=False, indent=2)


def find_device_by_id(registry: DeviceRegistry, device_id: str):
    """Find a device by its ID."""
    return next((d for d in registry.devices if d.device_id == device_id), None)


def add_device(device_id: str, device_name: str, device_description: str, 
               device_location: str, device_type: str, mqtt_topic: str, 
               capabilities: list = None, filepath: str = "devices.yaml"):
    """Add a new device to the registry."""
    try:
        registry = load_devices_from_yaml(filepath)
    except FileNotFoundError:
        # Create new registry if file doesn't exist
        registry = DeviceRegistry(devices=[])
    
    # Check if device already exists
    if find_device_by_id(registry, device_id):
        raise ValueError(f"Device with ID '{device_id}' already exists")
    
    # Create new device
    new_device = Device(
        device_id=device_id,
        device_name=device_name,
        device_description=device_description,
        device_location=device_location,
        device_type=device_type,
        mqtt_topic=mqtt_topic,
        capabilities=capabilities or []
    )
    
    # Add to registry
    registry.devices.append(new_device)
    
    # Save back to file
    save_devices_to_yaml(registry, filepath)
    return new_device


def update_device(device_id: str, filepath: str = "devices.yaml", **kwargs):
    """Update an existing device in the registry."""
    registry = load_devices_from_yaml(filepath)
    
    # Find the device
    device = find_device_by_id(registry, device_id)
    if not device:
        raise ValueError(f"Device with ID '{device_id}' not found")
    
    # Update device attributes
    for key, value in kwargs.items():
        if hasattr(device, key):
            setattr(device, key, value)
        else:
            raise ValueError(f"Invalid device attribute: {key}")
    
    # Save back to file
    save_devices_to_yaml(registry, filepath)
    return device


def delete_device(device_id: str, filepath: str = "devices.yaml"):
    """Delete a device from the registry."""
    registry = load_devices_from_yaml(filepath)
    
    # Find and remove the device
    original_count = len(registry.devices)
    registry.devices = [d for d in registry.devices if d.device_id != device_id]
    
    if len(registry.devices) == original_count:
        raise ValueError(f"Device with ID '{device_id}' not found")
    
    # Save back to file
    save_devices_to_yaml(registry, filepath)
    return True


if __name__ == "__main__":
    devices = load_devices_from_yaml("devices/devices.yaml")
    print(devices)
    print(f"="*100)
    # print(devices.devices[0])
    print(devices.devices[0].device_id)