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

    def __init__(self, edge_zone: float, exponent: float):
        edge_zone /= 100
        if (edge_zone >= 0.5):
            print("edge_zone cannot be more than 0.5 edge={}".format(edge_zone))
            edge_zone = 0.1
        self.edge_zone = edge_zone
        self.exponent = exponent

    # x = -0.5 .. 0.5
    # y = -0.5 .. 0.5
    def Process(self, x : float, y: float):
        r, theta = Transform._polar(x,y)
        range = 0.5 - self.edge_zone
        r /= range
        x, y = Transform._rect(range * (r ** self.exponent), theta)
        x = Transform._clamp(x, -0.5, 0.5)
        y = Transform._clamp(y, -0.5, 0.5)
        return x,y
