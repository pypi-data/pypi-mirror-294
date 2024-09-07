from typing import TypedDict
from .baseball_savant import StatCast


class PlayerDict(TypedDict):
    id: int
    firstname: str
    lastname: str
    slug: str
    url: str
    statcast: StatCast
