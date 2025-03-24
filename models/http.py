from typing import Any, Literal
from pydantic import BaseModel

from models.data import ConnectionConfig, DeviceConfig


class CommandRequest(BaseModel):
    command: str


class CommandResponse(BaseModel):
    error: str | None = None
    job_id: str | None = None


class GetStatusRequest(BaseModel):
    job_id: str


class GetStatusResponse(BaseModel):
    error: str | None = None
    status: str | None = None
    result: Any | None = None


class GetDevicesResponse(BaseModel):
    devices: dict[str, DeviceConfig]


class GetDeviceRequest(BaseModel):
    device_id: str


class GetDeviceResponse(BaseModel):
    error: str | None = None
    device: DeviceConfig | None = None


class RegisterDeviceRequest(BaseModel):
    name: str
    connection_type: Literal["serial", "tcp"]
    config: ConnectionConfig


class RegisterDeviceResponse(BaseModel):
    error: str | None = None
    device: DeviceConfig | None = None


class DeleteDeviceRequest(BaseModel):
    device_id: str


class DeleteDeviceResponse(BaseModel):
    error: str | None = None
