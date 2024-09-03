from pprint import pprint

from mtmaod.products._template import int2binarystring
from mtmaod.products.modis import MCD19A2Reader

# 读取MCD19A2数据文件指针
fp = MCD19A2Reader.open(r"test\testdata\MCD19A2.A2020001.h04v09.061.2023132152021.hdf")
# 查看所有数据集信息
pprint(MCD19A2Reader.list_datasets(fp, full=True))
# 读取某一数据集数据
dp = MCD19A2Reader.read(fp, "Optical_Depth_055", isRaw=False)
# 获取MCD19A2的波段过境时间
pprint(MCD19A2Reader.list_orbit_times(fp))
dp = MCD19A2Reader.read(fp, "AOD_QA", isRaw=False)
# 查看该数据集信息
pprint(dp.infos())
# 查看该数据集数据
print(dp[:])

# 获取QA波段指定bit位数的值
dp = MCD19A2Reader.read(fp, "AOD_QA", isRaw=True)
print(MCD19A2Reader.read_bit_fields(dp, 8, 12))

# 测试获取指定bit位数的值
print(int2binarystring(25645))
print(int2binarystring((25645 >> 8) % (2 ** (12 - 8)), 12 - 8))  # 该表达式与read_bit_fields函数原理相同
