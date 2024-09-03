import numpy as np
from mtmaod.utils.pyhdf import PyHDF, SDS
import pandas as pd

from .modis import MODISProductReader, MODISProductData


class MOD02Data(MODISProductData):

    def scale_and_offset(self, data: np.ndarray):
        infos: dict = self.infos()
        radiance_scales = MOD02Data.value_set_decimal(infos.get("reflectance_scales", 1), decimal=None)
        radiance_offsets = MOD02Data.value_set_decimal(infos.get("reflectance_offsets", 0), decimal=None)
        fill_value = infos.get("_FillValue")
        data = data.astype(np.float64)
        data[data == fill_value] = np.nan
        return radiance_scales * (data - radiance_offsets)


class MOD02Reader(MODISProductReader):
    Product_File_Time_Format = "[.]A%Y%j[.]%H%M[.]"
    LinkedDataClass = MOD02Data

    @staticmethod
    def table_scales_and_offsets(fp, *args, **kwargs):
        bands = ["EV_1KM_RefSB", "EV_1KM_Emissive", "EV_250_Aggr1km_RefSB", "EV_500_Aggr1km_RefSB"]
        columns = [
            "band_names",
            "reflectance_scales",
            "reflectance_offsets",
            "radiance_scales",
            "radiance_offsets",
            "corrected_counts_scales",
            "corrected_counts_offsets",
        ]
        indexes_string = "1,2,3,4,5,6,7,8,9,10,11,12,13lo,13hi,14lo,14hi,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36"
        indexes = indexes_string.split(",")
        df_list = []
        for band in bands:
            info = MOD02Reader.read(fp, band, *args, **kwargs).infos()
            info["band_names"] = info.get("band_names").split(",")
            _info = {k: info[k] for k in columns if k in info}
            df_list.append(pd.DataFrame(_info))
        return pd.concat(df_list, ignore_index=True).set_index("band_names").loc[indexes, :]
