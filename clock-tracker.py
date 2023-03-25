#!/usr/bin/env python3
# -*- mode: python -*-
import serial
import sys
import time


def main():
    while True:
        try:
            conn = serial.Serial(sys.argv[1], int(sys.argv[2]))
            while True:
                conn.write(b"command\r\n")
                data = b""
                while True:
                    data += conn.read(1)
                    if data[-1] == 10:
                        print(data)
                        break

        except serial.serialutil.SerialException:
            time.sleep(1)


if __name__ == '__main__':
    main()
