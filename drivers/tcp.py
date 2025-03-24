import asyncio
from drivers.base import BaseDriver


class TCPDriver(BaseDriver):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def send_command(self, command: str) -> str:
        await asyncio.sleep(0.5)  # Simulate TCP delay
        return f"[TCP @ {self.host}:{self.port}] {command} executed"
