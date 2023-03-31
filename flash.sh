#!/bin/bash
CORE=arduino:mbed_nano:nano33ble
CORE=arduino:mbed_rp2040:pico
arduino-cli upload -p $1 --fqbn $CORE clock-tracker.ino
