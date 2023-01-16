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

import argparse
import pyautogui

from src.config import Config
from src.virtualcontroller import VirtualController

def main():
    size = pyautogui.size()
    width = size[0]
    height = size[1]

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help="config file to load")
    parser.add_argument("--midi", "-m", type=int, help="Midi device to use")
    parser.add_argument("--list_midi", action="store_true", default=False, help="List Midi devices")

    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_argument("--frequency", type=int, required=False, default=30, choices=range(10,121), metavar="[10-120]", help="poll frequency")

    parser.add_argument("--center_zone", help="Percent of screen around center of screen that keeps yoke at 0,0", default=10, choices=range(0,101), metavar="[0-100]", type=int)
    parser.add_argument("--edge_zone", help="Percent of screen around center of screen that keeps yoke at 100", default=10, choices=range(0,101), metavar="[0-100]", type=int)

    parser.add_argument("--width", type=int, default=width, help="screen width")
    parser.add_argument("--height", type=int, default=height, help="screen height")
    parser.add_argument("--offset_x", type=int, default=0, help="mouse x offset in pixels")
    parser.add_argument("--offset_y", type=int, default=0, help="mouse y offset in pixels")


    options = parser.parse_args()

    if options.list_midi:
        return VirtualController.ListMidiDevices()

    if not options.config:
        print("You must specify a config")
        return -1

    config = Config()
    if not config.Load(options):
        print("Failed to load config")
        return -1

    controller = VirtualController(config, options)
    result = controller.Run()
    controller.Destroy()
    return result

if __name__ == '__main__':
	exit(main())
