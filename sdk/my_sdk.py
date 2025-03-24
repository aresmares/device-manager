import os
from dotenv import load_dotenv
import requests
from models.http import (
    CommandRequest,
    GetDeviceRequest,
    GetDeviceResponse,
    CommandResponse,
)

load_dotenv()


class MySDK:
    def __init__(self):
        self._device_daemon_host = None
        self._device_daemon_port = None

        self._device_manager_url = f"http://{os.environ["DEVICE_MANAGER_HOST"]}:{os.environ["DEVICE_MANAGER_PORT"]}"

    def connect_to_device(self, device_id: str) -> str:
        res = requests.get(
            f"{self._device_manager_url}/devices/{device_id}",
            data=GetDeviceRequest(device_id=device_id).model_dump_json(),
        )
        if res.status_code != 200:
            print(f"Failed to connect to device {device_id}, result: {res.text}")
            return f"Failed to connect to device {device_id}"

        resp = GetDeviceResponse.model_validate(res.json())
        if resp.error:
            print(resp.error)
            return f"Failed to connect to device {device_id}"

        assert resp.device is not None

        self._device_daemon_host = resp.device.daemon_url
        self._device_daemon_port = resp.device.daemon_port

        return "Connected to device"

    def send_command(self, command: str) -> str:
        if self._device_daemon_host is None or self._device_daemon_port is None:
            return "No device connected"

        print("sending command", command)

        req = CommandRequest(command=command)
        res = requests.post(
            f"http://{self._device_daemon_host}:{self._device_daemon_port}/send_command",
            data=req.model_dump_json(),
        )
        if res.status_code != 200:
            return f"Failed to send command, result: {res.text}"

        resp = CommandResponse.model_validate(res.json())
        if resp.error:
            return resp.error

        print("response", resp)
        return "Command sent successfully"


if __name__ == "__main__":
    sdk = MySDK()
    print(sdk.connect_to_device("test"))
    print(sdk.send_command("ls"))
