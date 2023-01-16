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

## Configuration

If you are using a midi controller find the midi bindings via:

```sh
python src/main.py --midi_test
```

Assuming you have midi controller the following config works for an M-Audio Oxygenpro Mini with Mouse Yoke active.

```
MOUSE_X 1 X
MOUSE_Y 1 Y
176.1 1 Z
176.33 1 RX
176.34 1 RY
176.35 1 RZ
176.36 1 SL0
176.37 1 SL1
137.40 1 1
153.40 1 1
137.41 1 2
153.41 1 2
137.42 1 3
153.42 1 3
137.43 1 MOUSE_TOGGLE
137.36 1 5
153.36 1 5
137.37 1 6
153.37 1 6
137.38 1 7
153.38 1 7
137.39 1 8
153.39 1 8
control.f12 1 MOUSE_TOGGLE
```

If you don't have a midi controller you can configure the virtual yoke as follows:

```
MOUSE_X 1 X
MOUSE_Y 1 Y
control.f12 1 MOUSE_TOGGLE
```

## Run

```sh
python src/main.py -m 1 -c src/oxygenpro.conf
```


## Inspiration

Parts of this code are inspired by

https://github.com/c0redumb/midi2vjoy

I needed a mouse yoke added and by the time I was done
the code looked nearly nothing like the original.