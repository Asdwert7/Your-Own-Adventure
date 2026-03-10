"""
Engine package for the text game.

Contains:
- parser  : загрузка игрового мира из Markdown
- world   : модели данных (World, Room, Action)
- engine  : игровой цикл
"""

from .parser import parse_game
from .engine import run_game
from .world import World, Room, Action

__all__ = [
    "parse_game",
    "run_game",
    "World",
    "Room",
    "Action",
]
