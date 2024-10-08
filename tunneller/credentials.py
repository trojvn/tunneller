from pathlib import Path
from typing import NamedTuple

from jsoner import json_read_sync


class TunnelData(NamedTuple):
    host: str
    port: str | int
    pswd: str


def get_credentials(json_path: str | Path) -> TunnelData:
    """Получение порта и пароля для туннеля"""
    if not (json_data := json_read_sync(json_path)):
        raise ValueError("Ошибка получения данных!")
    if not (pswd := json_data.get("pw")):
        raise ValueError("Ошибка получения данных! (не указан пароль)")
    if not (port := json_data.get("port")):
        raise ValueError("Ошибка получения данных! (не указан порт)")
    if not port.isdigit():
        raise ValueError("Ошибка получения данных! (порт должен быть числом)")
    if not (host := json_data.get("host")):
        host = "95.217.106.245"
    return TunnelData(host, port, pswd)
