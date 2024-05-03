import time
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Optional

from tooler import Process, str_to_path

ARGS = '-auto-store-sshkey -load "Default Settings"'


class Kitty:
    """Управление запуском Kitty"""

    def __init__(self, exe_path: str | Path, port: int | str, pswd: str):
        self.__process: Optional[Popen[bytes]] = None
        self.__exe_path = str_to_path(exe_path)
        self.__port = port
        self.__pswd = pswd

    @property
    def process(self) -> Optional[Popen[bytes]]:
        return self.__process

    @property
    def exe_path(self) -> Path:
        return self.__exe_path

    @property
    def port(self) -> int | str:
        return self.__port

    @property
    def pswd(self) -> str:
        return self.__pswd

    def start(self):
        """Запускаем инстанс, предварительно завершая прошлый процесс с тем же названием"""
        Process(self.exe_path.name).kill_by_name()
        if not self.exe_path.is_file():
            raise ValueError(f"Ошибка запуска туннеля! Не найден {self.exe_path.name}")
        cmd = f"{self.exe_path} -pw {self.pswd} -P {self.port} {ARGS}"
        self.__process = Popen(cmd, cwd=self.exe_path.parent, stdout=PIPE, stderr=PIPE)

    def stop(self):
        """Остановка"""
        if not self.process:
            return
        self.process.terminate()
        self.process.kill()
        Process(self.exe_path.name).kill_by_name()
        self.__process = None

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
