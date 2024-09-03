from mtmaod.products.modis import MXD04L2Reader
import psutil, os
import numpy as np

path = r"D:\code\imutum_aerosol_optical_depth\MOD04_L2.A2020001.0345.061.2020002233843.hdf"

ds = MXD04L2Reader.open(path)
band_names = MXD04L2Reader.list_datasets(ds)
print(band_names)
print("当前进程的内存使用：%.4f MB" % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

# band_aod = "Optical_Depth_Land_And_Ocean"
# data_aod = MXD04L2Reader.read(ds, band_aod)[:]
# print(data_aod.dtype, data_aod.shape)

data_lat = MXD04L2Reader.read(ds, MXD04L2Reader.Band_Latitude)[:]
print(data_lat)
print(data_lat.dtype, data_lat.shape)

data_lon = MXD04L2Reader.read(ds, MXD04L2Reader.Band_Longitude)[:]
print(data_lon)
print(data_lon.dtype, data_lon.shape)

print("当前进程的内存使用：%.4f MB" % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))


# import re

# infos = ds.attributes()["ArchiveMetadata.0"]
# gring_longitude = re.findall("GRINGPOINTLONGITUDE.*?\((.*?), (.*?), (.*?), (.*?)\).*?GRINGPOINTLONGITUDE", infos, re.S)[
#     0
# ]
# gring_latitude = re.findall("GRINGPOINTLATITUDE.*?\((.*?), (.*?), (.*?), (.*?)\).*?GRINGPOINTLATITUDE", infos, re.S)[0]
# print(coordinates)
