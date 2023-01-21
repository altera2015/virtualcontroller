#  Copyright 2023
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

import re


class Binding:

    MidiInputs = re.compile(r"\d+\.\d+")
    MouseInputs = {"MOUSE_X", "MOUSE_Y"}
    HotkeyInputs = re.compile("(\w+\.)?\w+\.\w+")


    def __init__(self, input: str, vjoy: int, output: str):
        self.input = input
        self.vjoy = vjoy
        self.output = output

    def IsMidi(self):
        return Binding.MidiInputs.match(self.input) is not None

    def IsHotKey(self):
        return self.input in Binding.MouseInputs

    def IsMouse(self):
        return Binding.HotkeyInputs.match(self.input) is not None

    def Validate(self) -> bool:
        if not (self.output in Config.Axis or self.output in Config.Buttons or self.output in Config.MouseOutputs):
            print("Invalid output specified {}".format(self.output))
            return False

        if not (self.output in Config.Axis or self.output in Config.Buttons or self.output in Config.MouseOutputs):
            print("Invalid output specified {}".format(self.output))
            return False

        if self.vjoy < 1 or self.vjoy > 16:
            print("Invalid VJoy index {}".format(self.vjoy))
            return False

        if not (self.IsMidi() or self.IsHotKey() or self.IsMouse() ):
            print("Unrecognized input binding {}".format(self.input))
            return False

        return True


class Config:

    Axis = {'X': 0x30, 'Y': 0x31, 'Z': 0x32, 'RX': 0x33, 'RY': 0x34, 'RZ': 0x35,
		'SL0': 0x36, 'SL1': 0x37, 'WHL': 0x38, 'POV': 0x39}

    Buttons = ['1','2','3','4','5','6','7','8','9', '10',
                '11','12', '13', '14', '15', '16', '17', '18', '19', '20',
                '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                '31', '32']

    MouseOutputs = ["MOUSE_TOGGLE", "MOUSE_RECENTER"]

    def __init__(self):
        self.bindings = {}
        self.vjoys = []

    def Load(self, options) -> bool:
        with open(options.config, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("#"):
                    continue
                values = line.split(" ")
                if len(values)==3:
                    input = values[0].upper()
                    vjoy = int(values[1])
                    output = values[2].strip().upper()

                    binding = Binding(input, vjoy, output)
                    if not binding.Validate():
                        continue

                    if not options.midi and binding.IsMidi():
                        print("Warning midi binding found without midi controller enabled: {}".format(binding.input))

                    self.bindings[values[0].upper()] = binding

                    if not (vjoy in self.vjoys):
                        self.vjoys.append(vjoy)
        return True

    def GetBinding(self, input) -> Binding:
        if input in self.bindings:
            return self.bindings[input]
        return None

    def GetVJoys(self) -> list:
        return self.vjoys
