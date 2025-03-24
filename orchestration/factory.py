from functools import cache
import os
from orchestration.processes import Processes


@cache
def get_orchestrator():
    orchestrator = os.getenv("ORCHESTRATOR", "processes")

    match orchestrator:
        case "processes":
            return Processes()
        case _:
            raise ValueError(f"Unsupported orchestator: {orchestrator}")
