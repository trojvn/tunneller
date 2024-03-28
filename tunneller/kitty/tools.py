from pathlib import Path
from shutil import rmtree, copyfile
from subprocess import run, PIPE
from typing import NamedTuple

from tooler import str_to_path

from .default import DEFAULT_SESSION_TEMPLATE


class LPort(NamedTuple):
    name: str
    port: int


class PrepareKitty:
    """Подготавливает Kitty директорию для запуска туннеля с нужными портами"""

    def __init__(
        self, host: str, cwd: str, name: str, rports: list[int], lports: list[LPort]
    ):
        self.__host = host
        self.__cwd = str_to_path(cwd)
        self.__name = name
        self.__rports = rports
        self.__lports = lports
        if not self.exe_path.exists():
            raise ValueError("kitty.exe не найден!")
        self.__create()

    @property
    def rports(self) -> list[int]:
        return self.__rports

    @property
    def lports(self) -> list[LPort]:
        return self.__lports

    @property
    def exe_path(self) -> Path:
        return Path("./kitty.exe")

    @property
    def host(self) -> str:
        return self.__host

    @property
    def cwd(self) -> Path:
        return self.__cwd

    @property
    def name(self) -> str:
        return self.__name  # m_kitty

    @property
    def name_dir(self) -> Path:
        return self.cwd / self.name

    @property
    def name_sessions_dir(self) -> Path:
        return self.name_dir / "Sessions"

    @property
    def name_exe(self) -> Path:
        return self.name_dir / f"{self.name}.exe"

    @property
    def default_settings(self) -> Path:
        return self.name_sessions_dir / "Default%20Settings"

    def __prepare_name_dir(self):
        run(f"taskkill /f /im {self.name}.exe", stdout=PIPE, stderr=PIPE)
        rmtree(self.name_dir, ignore_errors=True)
        self.name_dir.mkdir(parents=True, exist_ok=True)
        self.name_sessions_dir.mkdir(exist_ok=True)

    def __prepare_default_settings(self):
        rep_str = "PortForwardings\\"
        rep_str += ",".join([f"4R{p}=127.0.0.1%3A{p}" for p in self.rports])
        rep_str += ",".join([f"4L{p.port}={p.name}%3A{p.port}" for p in self.lports])
        rep_str += "\\"
        template = DEFAULT_SESSION_TEMPLATE.replace("95.217.106.245", self.host)
        with self.default_settings.open("w", encoding="utf-8") as f:
            f.write(template.replace(r"PortForwardings\\", rep_str))

    def __create(self):
        """Точка входа"""
        self.__prepare_name_dir()
        copyfile(self.exe_path, self.name_exe)
        self.__prepare_default_settings()
