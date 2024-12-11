from typing import NamedTuple


class LPort(NamedTuple):
    name: str
    server_port: int
    client_port: int
