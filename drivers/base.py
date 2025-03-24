from abc import ABC, abstractmethod


class BaseDriver(ABC):
    @abstractmethod
    async def send_command(self, command: str) -> str:
        pass
