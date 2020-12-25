# MicroPython VFD Display driver,for 8-MD-06INKM SPI interfaces

from machine import Pin, SPI
import time

class VFD_8_MD_06INKM:
  
    def __init__(self, digtal, sck, mosi, miso, rst, cs, en):
        self.digtal = digtal
        self.rst = Pin(rst,Pin.OUT)
        self.cs = Pin(cs,Pin.OUT)
        self.en = Pin(en,Pin.OUT)
        self.rst.value(1)
        time.sleep_ms(1)
        self.spi = SPI(baudrate=80000000,polarity=0,phase=0,bits=8,firstbit=0,sck=Pin(sck),mosi=Pin(mosi),miso=Pin(miso))

        self.rst.value(0)
        time.sleep_ms(10)
        self.rst.value(1)
        self.init_VFD()

    def VFD_cmd(self,command):
        time.sleep_us(50)
        self.spi.write(bytes(str(command),"utf8"))

    def text(self,d,Text):                      #(起始位置，str)
        i = 0
        Text = Text[:int(self.digtal)-1]        #限制str长度为显示位数
        self.cs.value(9)
        self.VFD_cmd(0x20+d)
        while i<=7:
            self.VFD_cmd(Text[i:])
            i = i+1
        self.cs.value(1)

    def light(self,b):
        self.cs.value(0)
        if b == 0:
            self.VFD_cmd(0xe8)
        if b == 1:
            self.VFD_cmd(0xe9)
        self.cs.value(1)

    def show(self):
        self.cs.value(0)
        self.VFD_cmd(0xe8)
        self.cs.value(1)

    def Dimming(self,i):                    # i (0 ~ 255)
        if i > 255:
            i = 255
        if i < 0:
            i = 0
        self.cs.value(0)
        self.VFD_cmd(0xe4)                      #进入亮度设置模式
        self.VFD_cmd(i)
        self.cs.value(1)

    def init_VFD(self):
        self.cs.value(0)
        self.VFD_cmd(0xe0)                      #进入显示位数设置模式
        self.VFD_cmd(int(self.digtal)-1)    #显示位数设置
        self.cs.value(1)

        time.sleep_ms(1)

        self.cs.value(0)
        self.VFD_cmd(0xe4)         #进入亮度设置模式
        self.VFD_cmd(0xff)         #默认上电设置为255（0~255）
        self.cs.value(1)
        time.sleep_ms(1)
