# virtualcontroller

## Introduction

* Input from Midi controller to Virtual Joystick
* Make mouse into a Virtual Yoke
* Input from Keyboard to virtual joystick

Great for flight simulators if you don't have a joystick yet.

## Setup

Install:

http://vjoystick.sourceforge.net

Install python requirements

```sh
python pip install -r requirements.txt
```

## Run

If you don't have any midi controllers, you can use the simple
Mouse Yoke example configuration:

```sh
python virtualcontroller.py -c mouseyoke.conf
```

If you have midi controllers, keep reading.

## Midi Configuration

If you are using a midi controller find the id you need to pass to the
-m parameter by listing the midi devices:

```sh
python src/main.py --list_midi
```

```
MIDI devices:
1 Oxygen Pro Mini
2 MIDIIN2 (Oxygen Pro Mini)
3 MIDIIN3 (Oxygen Pro Mini)
4 MIDIIN4 (Oxygen Pro Mini)
```

Say we want to pick the first with id "1", run:

```sh
copy mouseyoke.conf midi.conf
python virtualcontroller.py -c midi.conf -m 1 -v
```

any any time you press a button on the midi controller you should see a
warning about unbound messages:

```
Acquiring vJoystick: 1
x,y = 1.0, 0.509
Unbound message: 153.40
Unbound message: 137.40
```

You can now add the above button to the midi.conf and bind that button the
the first button on the second virtual joystick interface. The format
of the configuration file is:

<INPUT> <VJOY> <OUTPUT>

* INPUT can be any midi message, MOUSE_X, MOUSE_Y or a global hotkey.
* VJOY should be a number between 1 and the number of virtual joysticks
     configured.
* Output can be a number between 1 and 32, X, Y, Z, RX, RY, RZ, SL0, SL1, WHL, POV or
       MOUSE_TOGGLE

```
MOUSE_X 1 X
MOUSE_Y 1 Y
control.f12 1 MOUSE_TOGGLE
137.40 2 1
153.40 2 1
```

An example configuration is available in oxygenpro.conf

## Mouse Yoke config

The Mouse Yoke has a few configuration parameters:

* --width, screen width in pixels
* --height, screen height in pixels
* --center_zone, dead zone in center of screen in percent of min(width,height)
* --edge_zone, dead zone at edge of screen in percent of min(width, height)
* --offset_x x offset of the center of the virtual yoke
* --offset_y y offset of the center of the virtual yoke

## Global Hotkeys

If you need to toggle the mouse yoke on and off via the keyboard you can
use global hotkeys to do this. The list of key you can use
are available here:

https://pypi.org/project/global-hotkeys/

for example:

```
control.f12 1 MOUSE_TOGGLE
```

note: MOUSE_TOGGLE ignores the vjoy parameter, but pick an existing vjoy interface.

## Inspiration

Parts of this code are inspired by

https://github.com/c0redumb/midi2vjoy

I needed a mouse yoke added and by the time I was done
the code looked nearly nothing like the original.