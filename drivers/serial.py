from drivers.base import BaseDriver
import asyncio


class SerialDriver(BaseDriver):
    def __init__(self, port: int, baudrate: int):
        self.port = port
        self.baudrate = baudrate

    async def send_command(self, command: str) -> str:
        await asyncio.sleep(1)  # Simulate hardware I/O
        print(f"[Serial @ {self.port}] {command} executed")
        return f"[Serial @ {self.port}] {command} acknowledged"
