from abc import ABC, abstractmethod

from result import Result


class Orchestrator(ABC):
    _components = {}

    @abstractmethod
    def start_daemon(self, name: str, port: int, config_path: str) -> Result[None, str]:
        pass

    @abstractmethod
    def kill_deamon(self, name: str) -> Result[None, str]:
        pass

    @abstractmethod
    def get_hostname(self, name: str) -> Result[str, str]:
        pass

    def teardown(self) -> None:
        for name in self._components.copy():
            self.kill_deamon(name)
