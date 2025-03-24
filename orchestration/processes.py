import subprocess

from orchestration.base import Orchestrator
from result import Ok, Err, Result


class Processes(Orchestrator):
    _components: dict[str, subprocess.Popen] = {}

    def start_daemon(self, name: str, port: int, config_path: str) -> Result[None, str]:
        if name in self._components:
            return Err(f"A deamon with name {name} is already running")

        print(f"Starting driver daemon for {name}")
        process = subprocess.Popen(
            ["python", "device_daemon/daemon.py", config_path, "--port", str(port)]
        )

        self._components[name] = process
        return Ok(None)

    def kill_deamon(self, name: str) -> Result[None, str]:
        if name not in self._components:
            return Err(f"No deamon with name {name} is running")

        print(f"Killing {name}")
        self._components[name].kill()
        del self._components[name]
        return Ok(None)

    def get_hostname(self, name: str) -> Result[str, None]:
        return Ok("localhost")
