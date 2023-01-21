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

import os, time
import ctypes
import pyautogui
import pygame.midi
import time
import traceback
import winreg

from .transform import Transform
from .midicontroller import MidiController
from .config import Binding, Config
from .globalhotkey import GlobalHotkeys
from .message import Message
from .vector import Vector


class VirtualController:
    def __init__(self, config: Config, options):
        self.options = options
        self.config = config
        self.mouse_x_action = self.config.GetBinding("MOUSE_X")
        self.mouse_y_action = self.config.GetBinding("MOUSE_Y")
        self.mouse_enabled = self.mouse_x_action or self.mouse_y_action
        self.mouse_axis = [ 0.5, 0.5]
        self.last_mouse_axis = [ 0.0, 0.0 ]
        self.mouse = [0,0]

        self.mouse_actual = [0.0,0.0]
        self.mouse_offset = [0.0,0.0]
        self.mouse_disable_start = [0.0,0.0]

        self.screen_center = [options.width/2, options.height/2]
        self.offset = [self.options.offset_x, self.options.offset_y]

        vjoyregkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{8E31F76F-74C3-47F1-9550-E041EEDC5FBB}_is1')
        installpath = winreg.QueryValueEx(vjoyregkey, 'InstallLocation')
        winreg.CloseKey(vjoyregkey)
        dll_file = os.path.join(installpath[0], 'x64', 'vJoyInterface.dll')
        self.vjoy = ctypes.WinDLL(dll_file)

        for vid in config.GetVJoys():
            if options.verbose:
                print('Acquiring vJoystick:', vid)

            assert(self.vjoy.AcquireVJD(vid) == 1)
            assert(self.vjoy.GetVJDStatus(vid) == 0)
            self.vjoy.ResetVJD(vid)

        self.transform = Transform(options.edge_zone, options.exponent)
        self.midi = MidiController()

        self.hotkeys = GlobalHotkeys(config)

        self.handlers = {
            "MOUSE_TOGGLE" : self._MouseToggle,
            "MOUSE_RECENTER": self._MouseRecenter,
        }

        for axis in Config.Axis:
            self.handlers[axis] = self._AxisMove
        for button in Config.Buttons:
            self.handlers[button] = self._ButtonPress


    def _ButtonPress(self, binding: Binding, value: int):
        self.vjoy.SetBtn(value, binding.vjoy, int(binding.output))

    def _AxisMove(self, binding: Binding, value: int):
        value = (value + 1) << 8
        self.vjoy.SetAxis(value, binding.vjoy, Config.Axis[binding.output])

    def _MouseRecenter(self, binding: Binding, value: int):
        if value != 0:
            return
        self.mouse_offset[0] = 0.0
        self.mouse_offset[1] = 0.0
        pass

    def _MouseToggle(self, binding: Binding, value: int):
        if value != 0:
            return
        self.mouse_enabled = not self.mouse_enabled
        if not self.mouse_enabled:
            self.mouse_disable_start = Vector.Add( self.mouse, self.mouse_offset )
        else:
            self.mouse_offset = Vector.Sub(self.mouse_disable_start, self.mouse)

        if self.options.verbose:
            if self.mouse_enabled:
                print("Yoke Enabled")
            else:
                print("Yoke Disabled")

    def _ProcessYoke(self) -> bool:
        JOYSTICK_RANGE = 0x7fff
        if not (self.mouse_x_action or self.mouse_y_action):
            return False

        scaling = min(self.options.width, self.options.height)
        self.mouse[0], self.mouse[1] = pyautogui.position()
        Vector.AddInPlace(self.mouse, self.offset)

        if self.mouse_enabled:
            mouse = Vector.Add(self.mouse, self.mouse_offset)
            Vector.SubInPlace(mouse, self.screen_center)
            Vector.MultInPlace(mouse, 1/scaling)
            mouse[0], mouse[1] = self.transform.Process(mouse[0], mouse[1])
            mouse[0] += 0.5
            mouse[1] = 0.5 - mouse[1]
            Vector.Set(self.mouse_axis, mouse)

        if self.options.verbose:
            if Vector.LenSquare(self.mouse_axis, self.last_mouse_axis) > 0.01:
                print("x,y = {}, {}".format(round(self.mouse_axis[0], 3), round(self.mouse_axis[1],3)))
                Vector.Set(self.last_mouse_axis, self.mouse_axis)

        self.vjoy.SetAxis( int(self.mouse_axis[0]*JOYSTICK_RANGE), self.mouse_x_action.vjoy, Config.Axis[self.mouse_x_action.output])
        self.vjoy.SetAxis( int(self.mouse_axis[1]*JOYSTICK_RANGE), self.mouse_y_action.vjoy, Config.Axis[self.mouse_y_action.output])
        return True

    def _ProcessHotkeys(self) -> bool:
        message = self.hotkeys.Poll()
        if not message:
            return False
        self._HandleMessage(message)
        return True

    def _ProcessMidi(self) -> bool:
        message = self.midi.Poll()
        if not message:
            return False
        self._HandleMessage(message)
        return True

    def _HandleMessage(self, message: Message):
        binding = self.config.GetBinding(message.event)
        if binding:
            if binding.output in self.handlers:
                self.handlers[binding.output](binding, message.value)
            else:
                print("Unexpectedly didn't find a handler for this")
        else:
            if self.options.verbose:
                print("Unbound message: {}".format(message.event))

    def _Process(self):
        sleep_step_time = 1/120
        wait_time = 1 / self.options.frequency

        while True:
            # if used, process the virtual mouse yoke.
            self._ProcessYoke()

            # Process hotkey inputs
            self._ProcessHotkeys()

            # Process midi events for the remaining time.
            start = time.time()
            while ( time.time() - start < wait_time ):
                if not self._ProcessMidi():
                    time.sleep(sleep_step_time)

    def Run(self):
        try:
            if self.options.midi:
                self.midi.Start(self.options.midi)
            self.hotkeys.Start()
            self._Process()
        except KeyboardInterrupt:
            return 0
        except Exception as e:
            print("Error: {}".format(e))
            traceback.print_exc()
            return -1

    def Destroy(self):
        self.hotkeys.Destroy()
        self.midi.Destroy()
        for vid in self.config.GetVJoys():
            self.vjoy.RelinquishVJD(vid)


    def ListMidiDevices():
        pygame.midi.init()
        print('MIDI devices:')
        for i in range(pygame.midi.get_count()):
            info = pygame.midi.get_device_info(i)
            if info[2]:
                print(i, info[1].decode())
        pygame.midi.quit()
        return 0
