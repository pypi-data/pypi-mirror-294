from dask.array.core import Array as DaskArrayCoreArray
from numpydantic.interface.hdf5 import H5ArrayPath
from numpydantic.interface.hdf5 import H5Proxy
from pathlib import Path as PathlibPath
from cv2 import VideoCapture as Cv2VideoCapture
from numpydantic.interface.video import VideoProxy
from zarr.core import Array as ZarrCoreArray
from numpydantic.interface.zarr import ZarrArrayPath
from numpy import ndarray as Numpyndarray
import typing
import pathlib
NDArray = DaskArrayCoreArray | H5ArrayPath | typing.Tuple[typing.Union[pathlib.Path, str], str] | H5Proxy | PathlibPath | Cv2VideoCapture | VideoProxy | PathlibPath | ZarrCoreArray | ZarrArrayPath | Numpyndarray