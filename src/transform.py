#  Copyright 2023 (c)
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import math

class Transform:
    def _rect(r: float, theta: float):
        rad = math.radians(theta)
        x = r * math.cos(rad)
        y = r * math.sin(rad)
        return x,y

    def _polar(x:float, y:float):
        r = (x ** 2 + y ** 2) ** .5
        theta = math.degrees(math.atan2(y,x))
        return r, theta

    def _clamp(n:float, minn:float, maxn:float) -> float:
        return max(min(maxn, n), minn)

    def __init__(self, center_zone:float, edge_zone: float):
        center_zone /= 100
        edge_zone /= 100
        if (center_zone + edge_zone >= 0.5):
            print("center_zone + edge_zone cannot be more than 0.5 center={}, edge={}".format(center_zone, edge_zone))
            center_zone = 0.1
            edge_zone = 0.1

        center_zone /= 2.0
        self.center_zone = center_zone
        self.edge_zone = edge_zone
        self.slope = 0.5 / (0.5 - edge_zone  - center_zone )
        self.b = - self.slope * center_zone

    # x = -0.5 .. 0.5
    # y = -0.5 .. 0.5
    def Process(self, x : float, y: float):
        r, theta = Transform._polar(x,y)
        r = Transform._clamp(r, 0, 0.5 - self.edge_zone)
        if abs(r) < self.center_zone:
            return 0.0, 0.0
        else:
            return Transform._rect(r * self.slope + self.b, theta)
