from pyproj import Geod
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points


geod = Geod(ellps="WGS84")  # Your data may be from a different Geod.

line = LineString(((0, 0), (0, 1)))
point = Point(1, 1)

distance = geod.geometry_length(LineString(nearest_points(line, point)))

print(distance)