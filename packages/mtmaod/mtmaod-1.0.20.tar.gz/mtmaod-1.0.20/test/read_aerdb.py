from pprint import pprint

import numpy as np

from mtmaod.products.viirs import AERDBL2Reader

fp = AERDBL2Reader.open(r"test/testdata/AERDB_L2_VIIRS_SNPP.A2020001.0000.002.2023076102320.nc")
pprint(AERDBL2Reader.list_datasets(fp, full=True))
dp = AERDBL2Reader.read(fp, AERDBL2Reader.Band_Latitude, isRaw=False)
print(np.array(dp[:]))
dp = AERDBL2Reader.read(fp, AERDBL2Reader.Band_Longitude, isRaw=False)
print(np.array(dp[:]))
# dp = AERDBL2Reader.read(fp, "Optical_Depth_055", isRaw=False)
# pprint(AERDBL2Reader.list_orbit_times(fp))
# # pprint(dp.infos())
# print(dp[0, 1, 1])
