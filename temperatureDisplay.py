from machine import Pin, SPI, ADC
import sh1107
import gc
import sys
import time
import framebuf
import array

sensor=ADC(4)
led=Pin(25,Pin.OUT)
led.toggle()

#get temprature using pico onboard temperature sensor
def get_temp():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

#sun logo in bytes
icon_data=bytearray([0x00, 0xc0, 0x00, 0x00, 0xc0, 0x00, 0x00, 0xc0, 0x00, 0x10, 0x02, 0x00, 0x08, 0x04, 0x00, 0x03, 
0xf0, 0x00, 0x06, 0x18, 0x00, 0x04, 0x08, 0x00, 0xe4, 0x09, 0xc0, 0xe4, 0x09, 0xc0, 0x04, 0x08, 
0x00, 0x06, 0x18, 0x00, 0x03, 0xf0, 0x00, 0x08, 0x04, 0x00, 0x10, 0x02, 0x00, 0x00, 0xc0, 0x00, 
0x00, 0xc0, 0x00, 0x00, 0xc0, 0x00
])
frame = framebuf.FrameBuffer(icon_data, 18, 18, framebuf.MONO_HLSB)

print('Starting SH1107 SPI test')

# Initialize SPI
spi1 = SPI(1, baudrate=1_000_000, sck=Pin(14), mosi=Pin(15), miso=Pin(12))
print('SPI created: {} bytes free'.format(gc.mem_free()))

# Initialize the display
display = sh1107.SH1107_SPI(128, 64, spi1, dc=Pin(21), res=Pin(20), cs=Pin(13))
print('Display created: {} bytes free'.format(gc.mem_free()))

try:
    while True:       
        temp=get_temp()
        display.sleep(False)
        display.fill(0)
        display.text('Temperature: ', 0, 0, 1)
        display.text(''+str(temp)+' C',0,20,1)
        if temp>=30:
            display.text('it\'s too hot!', 0, 40, 1)
            display.blit(frame, 60, 15) 
        time.sleep(0.5)
        display.show()
    
except KeyboardInterrupt:
    print("Turning off display")
    display.fill(0)
    display.poweroff



