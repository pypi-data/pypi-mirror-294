import numpy as np

from easy_raster.transform.buffer_util import BufferUtil
from easy_raster.transform.normalizer import Normalizer


class RFactory:

    @staticmethod
    def heightmap(size: int, n: int = 5, seed: int = None):
        if seed is not None:
            np.random.seed(seed)
        height = np.zeros((size, size))
        weight = 0
        for i in range(n):
            amplitude = 2 ** i
            s = size // amplitude
            x = np.random.random((s, s))
            x = BufferUtil.smooth(x, sigma=3)
            x = BufferUtil.resize(x, width=size, height=size)
            x = 2 * np.abs(x - .5)
            height += x * amplitude
            weight += amplitude

        return Normalizer.normalize(height)

    @staticmethod
    def random_gradient(shape: tuple[int, ...], seed: int = None):
        if seed is not None:
            np.random.seed(seed)
        grad = np.exp(2j * np.pi * np.random.rand(*shape))
        grad = np.dstack([grad.real, grad.imag])
        return np.moveaxis(grad, 2, 0)
