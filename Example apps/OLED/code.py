import adafruit_bus_device.i2c_device as i2c_device
import board

# https://www.instructables.com/Graphics-on-a-SSD1306-I2C-OLED-128x64-Display-With/

# Turn on the VEXT
i2c = board.I2C()
device = i2c_device.I2CDevice(i2c, 0x74)

# HIGH is input, LOW is output
CONFIG_REGISTER = bytearray(4)
CONFIG_REGISTER[0] = 0x06
CONFIG_REGISTER[1] = 0b11111011
CONFIG_REGISTER[2] = 0x07
CONFIG_REGISTER[3] = 0b11111111

VALUE_REGISTER = bytearray(4)
VALUE_REGISTER[0] = 0x02
VALUE_REGISTER[1] = 0b00000000
VALUE_REGISTER[2] = 0x03
VALUE_REGISTER[1] = 0b00000100

with device as d:
    d.write(CONFIG_REGISTER, start=0, end=2)
    d.write(CONFIG_REGISTER, start=2, end=4)
    d.write(VALUE_REGISTER, start=0, end=2)
    d.write(VALUE_REGISTER, start=2, end=4)

i2c.deinit()

import sh1106
import busio
import board

# Create the I2C interface.
i2c = busio.I2C(board.I2C_SCL, board.I2C_SDA)

# # https://diyusthad.com/image2cpp
# with open('cat.bin', 'rb') as f:
#     data = bytearray(f.read())

# buffer = bytearray(((128 // 8) * 64) + 1)
# buffer[1:] = data

# Create the SH1106 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = sh1106.SH1106_I2C(128, 64, i2c)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
oled.pixel(1, 1, 1)
oled.show()