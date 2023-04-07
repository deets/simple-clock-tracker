# simple-clock-tracker

A very simple adaptive clock tracker to correct Arduino timestamps

## Hardware Setup

To measure timing difference and accuracy between several Arduinos,
you need to build and flash the contained firmware, and setup the
Arduinos with a shared trigger button. I use the usual small tactile
switches, like https://www.buildyourcnc.com/images/IMG_0333-800.JPG

It needs to be wired to GND and the two pins. The two Arduino GNDs
need to be connected, and they need each a pull-up resistor in the
several K-ohm range.

Adapt the sketch to contain the chosen input pin.

## Setup virtualenv

To install all the dependencies, you need a Python virtualenv. I use
`pipenv`, and if it works, all you need is `pipenv sync`. However it
has the tendency to be tricky when used on different platforms, so
instead create a virtualenv e.g. using `python -mvenv my-env`,
activate it, and install the requirements as usual.

## Install

To install, clone the repository and run

```
pip install -e .
```

This should create a command `clock-tracker` inside the virtualenv.

## Running clock-tracker

Run the `clock-tracker` command with the serial ports of your attached
arduinos as argument, e.g.

```
clock-tracker /dev/ttyUSB0 /dev/ttyUSB1
```

It should spit out a stream of timing estimate information. When the
Arduinos have a shared button attached, and the button is pressed, the
timestamps should show up and be within microseconds of each other.
