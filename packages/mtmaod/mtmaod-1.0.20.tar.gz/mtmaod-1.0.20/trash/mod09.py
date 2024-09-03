import numpy as np
from mtmaod.utils.pyhdf import PyHDF, SDS

from ._template import SatelliteProductReader, SatelliteProductData
from .modis import MODISProductReader, MODISProductData


class MOD09Data(MODISProductData):
    pass


class MOD09Reader(MODISProductReader):
    Product_File_Time_Format = "[.]A%Y%j[.]"
    LinkedDataClass = MOD09Data
