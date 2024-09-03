from dataclasses import dataclass

import numpy as np

from easy_raster.model.position import Position


@dataclass
class Resolution:
    width: int = 128
    height: int = 128

    @staticmethod
    def square(size: int):
        return Resolution.from_raw(size, size)

    @staticmethod
    def from_raw(height: int, width: int):
        return Resolution(width=width, height=height)

    def rescale_size(self, size: float) -> int:
        assert 0 <= size <= 1
        return int(size * self.width)

    def rescale_position(self, position: Position):
        return int(position.y * self.width), int(position.x * self.height)

    def area(self):
        return self.width * self.height

    def new_buffer(self, bands: int = None, dtype=None):
        if bands is None:
            return np.zeros((self.height, self.width), dtype=dtype)

        return np.zeros((self.height, self.width, bands))

    def raw(self):
        return self.height, self.width

    def __repr__(self):
        return f'{self.width}x{self.height}'

    def __str__(self):
        return repr(self)
