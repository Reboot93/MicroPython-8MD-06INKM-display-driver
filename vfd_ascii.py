'''
MicroPython Simple 8MD-06INKM Futaba VFD display driver

!! CGRAM coustomization is not provided

'''

from micropython import const

DCRAM_DATA_WRITE = const(0x20)
DGRAM_DATA_CLAER = const(0x10)
CGRAM_DATA_WRITE = const(0x40)
SET_DISPLAY_TIMING = const(0xE0)
SET_DIMMING_DATA = const(0xE4)
SET_DISPLAT_LIGHT_ON = const(0xE8)
SET_DISPLAT_LIGHT_OFF = const(0xEA)
SET_DISPLAT_LIGHT_DEBUG = const(0xEB)


class VFD():

    def __init__(self, spi, res, cs, en, digits=8, dimming=255, debug=False):
        self.rate = 5000000
        self.digits = digits
        self.dimming = dimming
        if debug:
            self.display_mode = SET_DISPLAT_LIGHT_DEBUG
        else:
            self.display_mode = SET_DISPLAT_LIGHT_ON
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        en.init(en.OUT, value=1)

        self.spi = spi
        self.res = res
        self.cs = cs
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
                (self.display_mode, 0x00)
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

    def set_display_dimming(self, dimming: int):
        dimming_data = dimming
        self.__write_cmd((SET_DIMMING_DATA, dimming_data))

    def __write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0, firstbit=self.spi.LSB)
        self.cs(1)
        self.cs(0)
        for i in cmd:
            self.spi.write(bytearray([i]))
        self.cs(1)

    def __write_data(self, buf: bytearray):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0, firstbit=self.spi.LSB)
        self.cs(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)