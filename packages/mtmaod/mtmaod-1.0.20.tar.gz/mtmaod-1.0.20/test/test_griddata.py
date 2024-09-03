import numpy as np
from geopy import distance

dlat = np.arange(9).reshape(3, 3)
dlon = np.arange(9).reshape(3, 3) + 5

print(np.column_stack((dlat.flatten(), dlon.flatten())))

step = 0.1
lat_min, lat_max = np.nanmin(dlat), np.nanmax(dlat)
lon_min, lon_max = np.nanmin(dlon), np.nanmax(dlon)
lat_min = np.floor(lat_min / step) * step
lat_max = np.ceil(lat_max / step) * step
lon_min = np.floor(lon_min / step) * step
lon_max = np.ceil(lon_max / step) * step
lat = np.arange(lat_min, lat_max + step, step)
lon = np.arange(lon_min, lon_max + step, step)
grid_lat, grid_lon = np.meshgrid(lat, lon)
print(grid_lat)
print(grid_lon)


a = distance.distance(kilometers=15).destination((32, 116), bearing=0)
b = distance.distance(kilometers=15).destination(a, bearing=90)
c = distance.distance(kilometers=15).destination(a, bearing=270)
print(a.latitude, a.longitude)
print(b.latitude, b.longitude)
print(c.latitude, c.longitude)
