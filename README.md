VFD display (8-MD-06INKM) simple driver

使用方法：

hspi = SPI(1, 5000000)
en = Pin(4)
rst = Pin(5)
cs = Pin(26)
display = VFD.VFD(hspi, rst, cs, en)

display.display_str(0, ‘12345678’)

display.clear() # 清除所有
display.clear(0) # 清除0位
