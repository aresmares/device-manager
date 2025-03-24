from abc import ABC, abstractmethod
import json
from typing import Any, TypeVar
from pydantic import BaseModel

TCommand = TypeVar("TCommand", bound="Command")


class Command[TCommand](ABC, BaseModel):
    @abstractmethod
    def serialize(self, cmd: TCommand) -> str: ...

    def deserialize(self, data: str) -> TCommand: ...


class SerialCommand(Command):
    command: str

    def serialize(self, cmd: "SerialCommand") -> str:
        return cmd.command

    def deserialize(self, data: str) -> "SerialCommand":
        return SerialCommand(command=data)


class CSharpCommand(Command):
    function: str
    kwargs: dict[str, Any]

    def serialize(self, cmd: "CSharpCommand") -> str:
        return f"{cmd.function} {cmd.kwargs}"

    def deserialize(self, data: str) -> "CSharpCommand":
        function, kwargs = data.split(" ", 1)

        return CSharpCommand(
            function=function,
            kwargs=json.loads(kwargs),
        )
