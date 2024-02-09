from pathlib import Path
from subprocess import PIPE, Popen, run
from typing import Optional

from tooler import str_to_path

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
        run(f"taskkill /f /im {self.exe_path.name}", stdout=PIPE, stderr=PIPE)
        self.__process = Popen(
            f"{self.exe_path} -pw {self.pswd} -P {self.port} {ARGS}",
            cwd=self.exe_path.parent,
            stdout=PIPE,
            stderr=PIPE,
        )

    def stop(self):
        """Остановка"""
        if not self.process:
            return
        self.process.terminate()
        self.process.kill()
        self.__process = None

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
