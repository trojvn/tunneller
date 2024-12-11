from pathlib import Path
from subprocess import PIPE, Popen

from tooler import Process

from ..base import BaseSSH
from ..models import LPort


class OpenSSH(BaseSSH):
    """Управление запуском SSH"""

    def __init__(
        self,
        exe_path: str | Path,
        host: str,
        port: int | str,
        pswd: str,
        rports: list[int],
        lports: list[LPort],
    ):
        super().__init__(exe_path, port, pswd)
        self.__host, self.__rports, self.__lports = host, rports, lports

    def start(self):
        """Запускаем инстанс, предварительно завершая прошлый процесс с тем же названием"""
        Process(self.exe_path.name).kill_by_name()
        if not self.exe_path.is_file():
            raise ValueError(f"Ошибка запуска туннеля! Не найден {self.exe_path.name}")
        args_rports = " ".join([f"-R {p}:{p}" for p in self.__rports])
        cmd = f"{self.exe_path} -p {self.port} trojvn@{self.__host}"
        cmd += " -oStrictHostKeyChecking=no"
        self.process = Popen(cmd, cwd=self.exe_path.parent, stdout=PIPE, stderr=PIPE)

    def stop(self):
        """Остановка"""
        if not self.process:
            return
        self.process.terminate()
        self.process.kill()
        Process(self.exe_path.name).kill_by_name()
        self.process = None

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
