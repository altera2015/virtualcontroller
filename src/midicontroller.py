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

import pygame
from .message import Message

class MidiController:
    def __init__(self):
        self.midi = None
        self.midi_index = None

    def Start(self, midi_index: int) -> bool:
        pygame.midi.init()
        self.midi_index = midi_index
        self.midi = pygame.midi.Input(self.midi_index)
        return True

    def Poll(self) -> Message:
        if not self.midi:
            return None
        if self.midi.poll():
            raw = self.midi.read(1)
            values = tuple(raw[0][0][0:3])
            if values[0] != 248:
                res = "{}.{}".format(values[0],values[1])
                return Message(res, values[2])
        return None

    def Destroy(self):
        if self.midi:
            self.midi.close()
            pygame.midi.quit()