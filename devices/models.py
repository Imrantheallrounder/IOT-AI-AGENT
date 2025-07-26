from pydantic import BaseModel, Field
from typing import List, Optional

class Device(BaseModel):
    device_id: str
    device_name: str
    device_description: str
    device_location: str
    device_type: str
    mqtt_topic: str
    capabilities: Optional[List[str]] = []  # e.g., ['on_off', 'brightness']

class DeviceRegistry(BaseModel):
    devices: List[Device]
