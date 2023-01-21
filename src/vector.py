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


class Vector:

    def AddInPlace(a:list, b:list) -> None:
        a[0]+=b[0]
        a[1]+=b[1]
    def SubInPlace(a:list, b:list) -> None:
        a[0]-=b[0]
        a[1]-=b[1]
    def MultInPlace(a:list, b:float) -> None:
        a[0]*=b
        a[1]*=b
    def Set(a:list, b:list) -> None:
        a[0] = b[0]
        a[1] = b[1]
    def Add( a: list, b: list) -> list:
        return [ a[0] + b[0], a[1] + b[1] ]
    def Sub( a: list, b: list):
        return [ a[0] - b[0], a[1] - b[1] ]
    def Mult( a: list, b: float) -> list:
        return [ a[0] * b, a[1] * b]
    def LenSquare(a:list, b:list) -> float:
        return (a[0] - b[0])**2 + (a[1] - b[1])**2
    def Copy( a: list ):
        return [a[0], a[1] ]
    def Print(s:str, a:list) -> None:
        print(s.format(round(a[0], 3), round(a[1],3)))