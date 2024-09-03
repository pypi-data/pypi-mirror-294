import warnings
from pathlib import Path

import numpy as np
import rasterio

from easy_raster.transform.normalizer import Normalizer

warnings.filterwarnings("ignore", module='rasterio')


class RasterIO:
    verbose = False

    @staticmethod
    def read(path: Path, band: int = None):
        with rasterio.open(str(path)) as _:
            data = _.read()
        if band is not None:
            data = data[band]
        return data

    @staticmethod
    def read_normalized(path: Path, band: int = None):
        return Normalizer.normalize(RasterIO.read(path, band))

    @staticmethod
    def write(path: Path | str, buffer: np.ndarray):
        path = Path(path)
        if RasterIO.verbose:
            from loguru import logger
            logger.debug(f'saving buffer {buffer.min():.3f}-{buffer.max():.3f} to {path}')

        path.parent.mkdir(parents=True, exist_ok=True)
        if buffer.ndim < 3:
            buffer = buffer[np.newaxis, :, :]
        depth, h, w = buffer.shape

        if buffer.dtype not in [np.uint8, np.uint16] and path.suffix.lower() in ['.png']:
            raise ValueError(
                'PNG only support uint8 or uint16. Tips: ImageIO.write_normalize() will handle float data type.'
            )

        with rasterio.open(str(path), 'w', width=w, height=h, count=depth, dtype=buffer.dtype) as _:
            _.write(buffer, indexes=[1 + i for i in range(depth)])

    @staticmethod
    def write_normalize(path: Path | str, data: np.ndarray):
        path = Path(path)
        data = Normalizer.normalize(data)

        if path.suffix == '.png':
            data = (data * 255).astype(np.uint8)

        RasterIO.write(path, data)
