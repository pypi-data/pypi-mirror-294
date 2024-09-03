import glob
import os

from mtmaod.products.modis import MCD19A2Reader

path = r"test\testdata\MCD19A2.2021183\*.hdf"
files = glob.glob(path)

center_file = r"test\testdata\MCD19A2.2021183\MCD19A2.A2021183.h26v04.061.2023148222736.hdf"
ds = MCD19A2Reader.open(center_file)
adjs = MCD19A2Reader.open_adjacent_files(center_file, files, (True, False, False, False))
print(adjs)
data = MCD19A2Reader.merge_adjascent_files(adjs, "Optical_Depth_055")
print(data)
