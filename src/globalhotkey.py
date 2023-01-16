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

import global_hotkeys
from config import Config, Binding
from message import Message
from threading import Lock

class GlobalHotkeyBinding:

    def __init__(self, hotkeys, binding: Binding):
        self.binding = binding
        self.hotkeys = hotkeys

    def TriggerDown(self):
        self.hotkeys.Insert(Message(self.binding, 1))

    def TriggerUp(self):
        self.hotkeys.Insert(Message(self.binding, 0))

class GlobalHotkeys:

    def __init__(self, config: Config):
        self.bindings = []
        self.messages = []
        self.mutex = Lock()

        for binding in config.bindings:
            if Binding.HotkeyInputs.match(binding) and not Binding.MidiInputs.match(binding):
                keys = binding.lower().split(".")
                print(keys)
                self.bindings.append( [keys, GlobalHotkeyBinding(self, binding).TriggerDown, GlobalHotkeyBinding(self, binding).TriggerUp] )
        if len(self.bindings)>0:
            global_hotkeys.register_hotkeys(self.bindings)
            global_hotkeys.start_checking_hotkeys()

    def Insert(self, message: Message):
        self.mutex.acquire()
        self.messages.append(message)
        self.mutex.release()

    def Start(self):
        if len(self.bindings)>0:
            global_hotkeys.register_hotkeys(self.bindings)
            global_hotkeys.start_checking_hotkeys()

    def Poll(self) -> Message:
        self.mutex.acquire()
        if len(self.messages) == 0:
            self.mutex.release()
            return None
        res = self.messages.pop(0)
        self.mutex.release()
        return res

    def Destroy(self):
        if len(self.bindings)>0:
            global_hotkeys.clear_hotkeys()
            global_hotkeys.stop_checking_hotkeys()

