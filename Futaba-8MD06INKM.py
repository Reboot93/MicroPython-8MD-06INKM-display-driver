'''
8MD-06INKM Futaba VFD display driver for MicroPython

====================================================
MIT License

Copyright (c) 2020 Reboot93

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import framebuf
from micropython import const

DCRAM_DATA_WRITE = const(0x20)
DGRAM_DATA_CLAER = const(0x10)
CGRAM_DATA_WRITE = const(0x40)
SET_DISPLAY_TIMING = const(0xE0)
SET_DIMMING_DATA = const(0xE4)
SET_DISPLAT_LIGHT_ON = const(0xE8)
SET_DISPLAT_LIGHT_OFF = const(0xEA)
SET_STAND_BY_MODE = const(0xEC)


class VFD(framebuf.FrameBuffer):

    def __init__(self, spi, res, cs, en, digits=8, dimming=255):
        self.rate = 5000000
        self.digits = digits
        self.dimming = dimming
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        en.init(en.OUT, value=1)

        self.spi = spi
        self.res = res
        self.cs = cs
        self.buffer = bytearray(5 * self.digits)
        super().__init__(self.buffer, 5 * self.digits, 7, framebuf.MONO_VLSB)
        import time

        # init VFD display
        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)
        time.sleep_ms(3)
        self.init_display()

    def init_display(self):
        for cmd in (
                # Set Display timing
                (SET_DISPLAY_TIMING, self.digits - 1),
                # Set the URAM (when digits > 16)
                # Set Display Dimming data
                (SET_DIMMING_DATA, self.dimming),
                # Release the All display OFF
                (SET_DISPLAT_LIGHT_ON, 0x00)
        ):
            self.__write_cmd(cmd)

    def display_claer(self, *address: int):
        if address:
            self.__write_cmd((DCRAM_DATA_WRITE | address, DGRAM_DATA_CLAER))
        else:
            for i in range(self.digits):
                self.__write_cmd((DCRAM_DATA_WRITE | i, DGRAM_DATA_CLAER))

    def display_str(self, address: int, msg: str):
        for i in msg:
            self.__write_cmd((DCRAM_DATA_WRITE | address, ord(i)))
            if address < self.digits - 1:
                address += 1
            else:
                break

    def display_custom(self, address: int, buf: bytearray):
        self.__write_data(address, buf)
        self.__write_cmd((DCRAM_DATA_WRITE | address, address))

    def show(self):
        buf = bytearray(5)
        fbuf = framebuf.FrameBuffer(buf, 5, 7, framebuf.MONO_VLSB)
        for i in range(self.digits):
            fbuf.fill(0)
            fbuf.blit(self, 0 - (i * 5), 0)
            self.__write_data(i, buf)
        for i in range(self.digits):
            self.__write_cmd((DCRAM_DATA_WRITE | i, i))

    def set_display_dimming(self, dimming: int):
        dimming_data = dimming
        self.__write_cmd((SET_DIMMING_DATA, dimming_data))

    def on(self):
        self.__write_cmd([SET_STAND_BY_MODE, 0x00])

    def off(self):
        self.__write_cmd([SET_STAND_BY_MODE | 1, 0x00])

    def __write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0, firstbit=self.spi.LSB)
        self.cs(1)
        self.cs(0)
        for i in cmd:
            self.spi.write(bytearray([i]))
        self.cs(1)

    def __write_data(self, address: int, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0, firstbit=self.spi.LSB)
        self.cs(1)
        self.cs(0)
        self.spi.write(bytearray([CGRAM_DATA_WRITE | address]))
        for i in buf:
            self.spi.write(bytearray([i]))
        self.cs(1)