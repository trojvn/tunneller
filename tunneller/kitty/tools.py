from pathlib import Path
from shutil import rmtree, copyfile
from subprocess import run, PIPE
from typing import NamedTuple

from .default import DEFAULT_SESSION_TEMPLATE


class LPort(NamedTuple):
    name: str
    port: int


class PrepareKitty:
    """Подготавливает Kitty директорию для запуска туннеля с нужными портами"""

    def __init__(self, name: str, rports: list[int], lports: list[LPort]):
        self.__exe_path = Path("./kitty.exe")
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
        return self.__exe_path

    @property
    def name(self) -> str:
        return self.__name  # m_kitty

    @property
    def name_dir(self) -> Path:
        return Path(self.name)

    @property
    def name_sessions_dir(self) -> Path:
        return self.name_dir / "Sessions"

    @property
    def name_exe(self) -> Path:
        return self.name_dir / f"{self.name}.exe"

    @property
    def default_settings(self) -> Path:
        return self.name_dir / "Default%20Settings"

    def __prepare_name_dir(self):
        run(f"taskkill /f /im {self.name}.exe", stdout=PIPE, stderr=PIPE)
        rmtree(self.name_dir, ignore_errors=True)
        self.name_dir.mkdir(exist_ok=True)
        self.name_sessions_dir.mkdir(exist_ok=True)

    def __prepare_default_settings(self):
        replace_str = "PortForwardings\\"
        replace_str += [f"4R{p}=127.0.0.1%3A{p}," for p in self.rports]
        replace_str += [f"4L{p.port}={p.name}%3A{p.port}," for p in self.lports]
        replace_str = replace_str[:-1]
        replace_str += "\\"
        with self.default_settings.open("w", encoding="utf-8") as f:
            f.write(DEFAULT_SESSION_TEMPLATE.replace(r"PortForwardings\\", replace_str))

    def __create(self):
        """Точка входа"""
        self.__prepare_name_dir()
        copyfile(self.exe_path, self.name_exe)
        self.__prepare_default_settings()
