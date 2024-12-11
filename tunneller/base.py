from pathlib import Path
from subprocess import Popen


class BaseSSH:
    def __init__(self, exe_path: str | Path, port: int | str, pswd: str):
        self.__process: Popen[bytes] | None = None
        self.__exe_path = Path(exe_path)
        self.__port = port
        self.__pswd = pswd

    @property
    def process(self) -> Popen[bytes] | None:
        return self.__process

    @process.setter
    def process(self, value: Popen[bytes] | None):
        self.__process = value

    @property
    def exe_path(self) -> Path:
        return self.__exe_path

    @property
    def port(self) -> int | str:
        return self.__port

    @property
    def pswd(self) -> str:
        return self.__pswd
