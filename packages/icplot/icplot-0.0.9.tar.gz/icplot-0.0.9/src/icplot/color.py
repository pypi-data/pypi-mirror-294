"""
This module handles colors
"""

from typing import Callable

from iccore.serialization import Serializable


class Color(Serializable):
    """
    A color class, internal storage is rgba as float.
    """

    def __init__(self, r: float = 0.0, g: float = 0.0, b: float = 0.0, a: float = 1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @staticmethod
    def from_list(data: list):
        return Color(data[0], data[1], data[2])

    def serialize(self):
        return {"r": self.r, "g": self.g, "b": self.b, "a": self.a}

    def as_list(self) -> list:
        return [self.r, self.g, self.b]

    def is_black(self) -> bool:
        return self.r == 0.0 and self.g == 0.0 and self.b == 0.0 and self.a == 1.0


class ColorMap:
    """
    A mapping from a flat index to a color
    """

    def __init__(self, label: str, data_func: Callable):
        self.label = label
        self.data_func = data_func
        self.start_offset = 0.25
        self.scale = 2

    def get_color(self, cursor: int, values: list) -> Color:
        """
        Returns a colour based on a cmap and how far across
        the datasets you are
        """
        position = cursor / len(values)
        return Color.from_list(
            self.data_func(self.start_offset + (position / self.scale))
        )
