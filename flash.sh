#!/bin/bash
CORE=arduino:mbed_nano:nano33ble
CORE=arduino:mbed_rp2040:pico
arduino-cli upload -p /dev/ttyACM0 --fqbn $CORE clock-tracker.ino
