from mtmaod.products.viirs import AERDBL2Reader
from pprint import pprint

fp = AERDBL2Reader.open(r"test/testdata/AERDT_L2_VIIRS_SNPP.A2020001.0512.002.2023214032031.nc")
pprint(AERDBL2Reader.list_datasets(fp, full=True))
# dp = AERDBL2Reader.read(fp, "Optical_Depth_055", isRaw=False)
# pprint(AERDBL2Reader.list_orbit_times(fp))
# # pprint(dp.infos())
# print(dp[0, 1, 1])
