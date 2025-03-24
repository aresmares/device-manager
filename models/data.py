from pydantic import BaseModel
from typing import Literal, Union

type ConnectionConfig = Union[SerialDriverConfig, TCPDriverConfig]


class SerialDriverConfig(BaseModel):
    port: str
    baudrate: int


class TCPDriverConfig(BaseModel):
    host: str
    port: int


class DeviceConfig(BaseModel):
    type: Literal["serial", "tcp"]
    daemon_url: str = "localhost"
    daemon_port: int
    driver_config: ConnectionConfig


class DevicesFile(BaseModel):
    devices: dict[str, DeviceConfig]


class JobStatus(BaseModel):
    status: Literal["pending", "done", "error", "in_progress", "queued", "unknown"]
    result: str | None = None
    error: str | None = None
