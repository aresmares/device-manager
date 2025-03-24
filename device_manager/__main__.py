import os
from dotenv import load_dotenv
from fastapi import FastAPI
from result import Err, Ok
import yaml
from models.data import DeviceConfig
from models.http import (
    DeleteDeviceRequest,
    DeleteDeviceResponse,
    GetDeviceRequest,
    GetDeviceResponse,
    GetDevicesResponse,
    RegisterDeviceRequest,
    RegisterDeviceResponse,
)
from orchestration.factory import get_orchestrator

load_dotenv()


async def teardown():
    orchestrator = get_orchestrator()
    orchestrator.teardown()


app = FastAPI(on_shutdown=[teardown])

config: dict[str, DeviceConfig] = {}

LATEST_DAEMON_PORT = 8000


@app.get("/devices")
def list_devices() -> GetDevicesResponse:
    return GetDevicesResponse(devices=config)


@app.get("/devices/{name}")
def get_device(req: GetDeviceRequest) -> GetDeviceResponse:
    name = req.device_id
    device = config.get(name)
    if not device:
        return GetDeviceResponse(error="Device not found")
    return GetDeviceResponse(device=device)


@app.put("/devices/{name}")
def register_device(req: RegisterDeviceRequest) -> RegisterDeviceResponse:
    global LATEST_DAEMON_PORT
    if req.name in config:
        return RegisterDeviceResponse(error="Device already exists")

    if req.config in [conf.driver_config for conf in config.values()]:
        return RegisterDeviceResponse(
            error="Device config already exists with another name"
        )

    LATEST_DAEMON_PORT += 1

    new_device = DeviceConfig(
        type=req.connection_type,
        daemon_port=LATEST_DAEMON_PORT,
        driver_config=req.config,
    )

    path = f"/tmp/{req.name}_config.yaml"
    with open(path, "w") as f:
        yaml.dump(new_device.model_dump(), f)

    orchestrator = get_orchestrator()
    res = orchestrator.start_daemon(req.name, new_device.daemon_port, path)
    if res.is_err():
        return RegisterDeviceResponse(error=res.err())

    res = orchestrator.get_hostname(req.name)
    match res:
        case Err(e):
            return RegisterDeviceResponse(error=e)
        case Ok(hostname):
            new_device.daemon_url = hostname

    config[req.name] = new_device

    return RegisterDeviceResponse(device=new_device)


@app.delete("/devices/{name}")
def delete_device(name: str, _: DeleteDeviceRequest) -> DeleteDeviceResponse:
    if name not in config:
        return DeleteDeviceResponse(error="Device not found")

    orchestrator = get_orchestrator()
    res = orchestrator.kill_deamon(name)
    if res.is_err():
        return DeleteDeviceResponse(error=res.err())

    del config[name]
    return DeleteDeviceResponse()


if __name__ == "__main__":
    import uvicorn

    host = os.environ["DEVICE_MANAGER_HOST"]
    port = int(os.environ["DEVICE_MANAGER_PORT"])

    uvicorn.run(app, host=host, port=port)
