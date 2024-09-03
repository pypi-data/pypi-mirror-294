import numpy as np

MAX_PIXEL_VALUE = 255


class BufferUtil:
    @staticmethod
    def mirror_tile(buffer: np.ndarray):
        top = np.hstack([buffer, np.fliplr(buffer)])
        return np.vstack([top, np.flipud(top)])

    @staticmethod
    def normalize(buffer: np.ndarray, png_format: bool = False):
        if buffer.min() != buffer.max():
            buffer -= buffer.min()
        if buffer.max() != 0:
            buffer = buffer / buffer.max()

        if png_format:
            buffer = (buffer * MAX_PIXEL_VALUE).astype('uint8')
        else:
            buffer = buffer.astype('float32')

        return buffer

    @staticmethod
    def resize(buffer: np.ndarray, width: int, height: int, seamless: bool = False):
        import skimage

        res = skimage.transform.resize(buffer, (height, width), anti_aliasing=True)

        if seamless:
            res[-1, :] = res[0, :]
            res[:, -1] = res[:, 0]

        return res

    @staticmethod
    def smooth(buffer: np.ndarray, sigma: float = 1):
        from scipy.ndimage import gaussian_filter

        return gaussian_filter(buffer, sigma=sigma, order=0)
