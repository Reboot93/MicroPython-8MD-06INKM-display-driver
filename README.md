# Futaba VFD display (8-MD-06INKM) driver for MicroPython (Framebuf)

[![Sample video](https://res.cloudinary.com/marcomontalbano/image/upload/v1659263094/video_to_markdown/images/youtube--nW1mT3Vwk4U-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=nW1mT3Vwk4U "Sample video")

## Usage sample
**使用示例：**
``` python
import framebuf, futaba_8md06inkm, time
from machine import Pin, freq, SPI

freq(240000000)

hspi = SPI(1, 5000000)
en = Pin(4)
rst = Pin(5)
cs = Pin(26)
display = Futaba_8MD06INKM.VFD(hspi, rst, cs, en)
```
### Framebuf base display
基于Framebuf显示
``` python
display.fill(0)
display.text('Reboot93', i, 0)
display.show()
``` 

### Display built-in charaters (Similar ssd1306)
显示内置字符 (类似ssd1306)
``` python
display.display_str(0, ‘12345678’) # Starting at block 0 display '12345678'
                                   # 从0位开始显示'12345678'
                                   # Only characters that already exist in the CGRAM can be display
                                   # 只能显示CGRAM中已经存在的字符
```
### Customize the display content in a single block
自定义单块显示内容
``` python
buf = bytearray(5)
fbuf = framebuf.FrameBuffer(buf, 5, 7, framebuf.MONO_VLSB)
fbuf.rect(0, 0, 5, 7, 1)
display.display_custom(0，buf)
```
### Clear the display
清除显示内容
``` python
display.clear() # 清除所有 clear all
display.clear(0) # 清除0位 clear block 0
```
### Set the luminance
设置亮度
``` python
display.set_display_dimming(255) # 0~255
``` 
### Turn the display on or off(Stand-by mode)
开/关屏幕
``` python
display.on()
display.off()
``` 
