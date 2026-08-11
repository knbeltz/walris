from pydantic import BaseModel


class DeviceTokenRegistration(BaseModel):
    expo_push_token: str
    device_id: str
    platform: str
    timezone: str
