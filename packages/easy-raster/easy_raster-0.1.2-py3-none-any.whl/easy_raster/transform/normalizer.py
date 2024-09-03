import numpy as np


class Normalizer:
    @staticmethod
    def identity(x: np.ndarray):
        return x

    @staticmethod
    def log_scale(x: np.ndarray):
        y = x - x.min()
        try:
            return np.log10(y + 1)
        except Exception as e:
            print(y)
            raise e

    @staticmethod
    def power(y: float):
        def func(x: np.ndarray):
            return np.power(x, y)

        return func

    @staticmethod
    def normalize(x: np.ndarray):
        a, b = x.min(), x.max()

        if np.any(b == 0):
            return x

        return (x - a) / (b - a)
