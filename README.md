# MicroPython-VFD-display-simple-drive
VFD display (8-MD-06INKM) simple driver

使用方法：

hspi = SPI(1, 5000000)
en = Pin(4)    # data/command
rst = Pin(5)   # reset
cs = Pin(26)   # chip select, some modules do not have a pin for this
display = VFD.VFD(hspi, rst, cs, en)

display.display_str(0, ‘12345678’)

display.clear() # 清除所有
display.clear(0) # 清除0位
