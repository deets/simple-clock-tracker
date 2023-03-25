#!/bin/bash
CORE=arduino:mbed_nano:nano33ble
CORE=arduino:mbed_rp2040:pico
arduino-cli compile --fqbn "$CORE" clock-tracker.ino
